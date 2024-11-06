# backend/api/execute.py

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.execution import Execution
from models import db
from schemas.execute_schema import ExecuteSchema
import subprocess
import datetime

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

        # Save execution details to the database
        execution = Execution(
            user_id=get_jwt_identity(),
            language=language.lower(),
            code=code,
            output=output,
            error=error,
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(execution)
        db.session.commit()

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
