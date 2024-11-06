# # backend/api/execute.py

# from flask import Blueprint, request, jsonify, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models.execution import Execution
# from models import db
# from schemas.execute_schema import ExecuteSchema
# import subprocess
# import datetime

# execute_bp = Blueprint('execute', __name__)
# execute_schema = ExecuteSchema()

# @execute_bp.route('/', methods=['POST'])
# @jwt_required()
# def execute_code():
#     """
#     Endpoint to execute code snippets in supported languages.
#     """
#     json_data = request.get_json()

#     # Validate and deserialize input
#     try:
#         data = execute_schema.load(json_data)
#     except ValidationError as err:
#         return jsonify(err.messages), 400

#     language = data['language']
#     code = data['code']

#     # Define the command based on language
#     if language.lower() == 'python':
#         cmd = ['python3', '-c', code]
#     elif language.lower() == 'javascript':
#         cmd = ['node', '-e', code]
#     else:
#         # This should not occur due to validation
#         return jsonify({'error': 'Unsupported language.'}), 400

#     try:
#         # Execute the code with a timeout of 5 seconds
#         result = subprocess.run(
#             cmd,
#             capture_output=True,
#             text=True,
#             timeout=5
#         )
#         output = result.stdout
#         error = result.stderr

#         # Save execution details to the database
#         execution = Execution(
#             user_id=get_jwt_identity(),
#             language=language.lower(),
#             code=code,
#             output=output,
#             error=error,
#             created_at=datetime.datetime.utcnow()
#         )
#         db.session.add(execution)
#         db.session.commit()

#         # Prepare the response
#         response = {
#             'id': execution.id,
#             'output': output,
#             'error': error
#         }

#         return jsonify(response), 200

#     except subprocess.TimeoutExpired:
#         current_app.logger.error('Execution timed out for user ID: %s', get_jwt_identity())
#         return jsonify({'error': 'Execution timed out.'}), 400
#     except subprocess.CalledProcessError as e:
#         current_app.logger.exception('Subprocess error for user ID: %s', get_jwt_identity())
#         return jsonify({'error': 'An error occurred during code execution.'}), 400
#     except Exception as e:
#         current_app.logger.exception('Unexpected error for user ID: %s', get_jwt_identity())
#         return jsonify({'error': 'An unexpected error occurred.'}), 400

# @execute_bp.route('/history', methods=['GET', 'OPTIONS'])  # Allow OPTIONS method
# @jwt_required()
# def get_history():
#     if request.method == 'OPTIONS':
#         return jsonify({'message': 'OK'}), 200

#     user_id = get_jwt_identity()
#     executions = Execution.query.filter_by(user_id=user_id).all()
#     history = [{
#         'id': exec.id,
#         'language': exec.language,
#         'code': exec.code,
#         'output': exec.output,
#         'error': exec.error,
#         'created_at': exec.created_at.isoformat()
#     } for exec in executions]

#     return jsonify(history), 200

# backend/api/execute.py

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.execution import Execution
from models import db
from schemas.execute_schema import ExecuteSchema
import subprocess
import datetime
from marshmallow import ValidationError
from utils.storage import upload_execution_result, get_execution_result

execute_bp = Blueprint('execute', __name__)
execute_schema = ExecuteSchema()

@execute_bp.route('/', methods=['POST'])
@jwt_required()
def execute_code():
    """
    Endpoint to execute code snippets in supported languages.
    """
    json_data = request.get_json()

    # Validate and deserialize input
    try:
        data = execute_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    language = data['language']
    code = data['code']
    user_id = get_jwt_identity()

    # Define the command based on language
    if language.lower() == 'python':
        cmd = ['python3', '-c', code]
    elif language.lower() == 'javascript':
        cmd = ['node', '-e', code]
    else:
        # This should not occur due to validation
        return jsonify({'error': 'Unsupported language.'}), 400

    try:
        # Execute the code with a timeout of 5 seconds
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        error = result.stderr

        # Save execution details to the database without setting 'id'
        execution = Execution(
            user_id=user_id,
            language=language.lower(),
            code=code,
            output=output if output else '',
            error=error if error else '',
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(execution)
        db.session.commit()

        # After commit, 'execution.id' is populated by the database
        upload_success = upload_execution_result(execution.id, {
            'id': execution.id,  # Now an integer
            'user_id': user_id,
            'language': language,
            'code': code,
            'output': execution.output,
            'error': execution.error,
            'created_at': execution.created_at.isoformat()
        })

        if not upload_success:
            current_app.logger.error(f"Failed to upload execution {execution.id} to S3.")
            return jsonify({'error': 'Failed to upload results to storage.'}), 500

        # Prepare the response
        response = {
            'id': execution.id,
            'output': output,
            'error': error
        }

        return jsonify(response), 200

    except subprocess.TimeoutExpired:
        current_app.logger.error('Execution timed out for user ID: %s', get_jwt_identity())
        return jsonify({'error': 'Execution timed out.'}), 400
    except subprocess.CalledProcessError as e:
        current_app.logger.exception('Subprocess error for user ID: %s', get_jwt_identity())
        return jsonify({'error': 'An error occurred during code execution.'}), 400
    except Exception as e:
        current_app.logger.exception('Unexpected error for user ID: %s', get_jwt_identity())
        return jsonify({'error': 'An unexpected error occurred.'}), 400

@execute_bp.route('/history', methods=['GET', 'OPTIONS'])  # Allow OPTIONS method
@jwt_required()
def get_history():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    user_id = get_jwt_identity()
    executions = Execution.query.filter_by(user_id=user_id).all()
    history = [{
        'id': exec.id,
        'language': exec.language,
        'code': exec.code,
        'output': exec.output,
        'error': exec.error,
        'created_at': exec.created_at.isoformat()
    } for exec in executions]

    return jsonify(history), 200
