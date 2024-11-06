# import docker
# import uuid
# import os
# import tempfile
# import shutil

# from config import Config

# docker_client = docker.from_env()

# LANGUAGES = {
#     'python': {
#         'image': 'python:3.10-slim',
#         'extension': '.py',
#         'command': 'python {filename}'
#     },
#     'c': {
#         'image': 'gcc:latest',
#         'extension': '.c',
#         'compile_command': 'gcc {filename} -o {output}',
#         'execute_command': './{output}'
#     },
#     'java': {
#         'image': 'openjdk:17-slim',
#         'extension': '.java',
#         'compile_command': 'javac {filename}',
#         'execute_command': 'java {classname}'
#     },
#     'javascript': {
#         'image': 'node:16-slim',
#         'extension': '.js',
#         'command': 'node {filename}'
#     },
#     # Add more languages as needed
# }

# def execute_code(language, code):
#     if language not in LANGUAGES:
#         return {'error': 'Unsupported language'}

#     config = LANGUAGES[language]
#     file_extension = config['extension']
#     filename = f'Main{file_extension}'
#     unique_id = str(uuid.uuid4())
#     temp_dir = tempfile.mkdtemp()
#     file_path = os.path.join(temp_dir, filename)

#     with open(file_path, 'w') as f:
#         f.write(code)

#     try:
#         if language == 'c':
#             # Compile C code
#             compile_cmd = config['compile_command'].format(filename=filename, output='a.out')
#             compile_result = docker_client.containers.run(
#                 config['image'],
#                 compile_cmd,
#                 volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
#                 working_dir='/usr/src/app',
#                 network_disabled=True,
#                 mem_limit='50m',
#                 stderr=True,
#                 stdout=True,
#                 detach=False,
#                 remove=True,
#                 timeout=Config.EXECUTION_TIMEOUT
#             )
#             if compile_result.decode().strip() != '':
#                 return {'error': compile_result.decode()}
#             # Execute compiled C program
#             exec_cmd = config['execute_command'].format(output='a.out')
#             exec_result = docker_client.containers.run(
#                 config['image'],
#                 exec_cmd,
#                 volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
#                 working_dir='/usr/src/app',
#                 network_disabled=True,
#                 mem_limit='50m',
#                 stderr=True,
#                 stdout=True,
#                 detach=False,
#                 remove=True,
#                 timeout=Config.EXECUTION_TIMEOUT
#             )
#             output = exec_result.decode()
#             return {'output': output}
#         elif language == 'java':
#             # Compile Java code
#             classname = 'Main'
#             compile_cmd = config['compile_command'].format(filename=filename)
#             compile_result = docker_client.containers.run(
#                 config['image'],
#                 compile_cmd,
#                 volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
#                 working_dir='/usr/src/app',
#                 network_disabled=True,
#                 mem_limit='100m',
#                 stderr=True,
#                 stdout=True,
#                 detach=False,
#                 remove=True,
#                 timeout=Config.EXECUTION_TIMEOUT
#             )
#             if compile_result.decode().strip() != '':
#                 return {'error': compile_result.decode()}
#             # Execute Java program
#             exec_cmd = config['execute_command'].format(classname=classname)
#             exec_result = docker_client.containers.run(
#                 config['image'],
#                 exec_cmd,
#                 volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
#                 working_dir='/usr/src/app',
#                 network_disabled=True,
#                 mem_limit='100m',
#                 stderr=True,
#                 stdout=True,
#                 detach=False,
#                 remove=True,
#                 timeout=Config.EXECUTION_TIMEOUT
#             )
#             output = exec_result.decode()
#             return {'output': output}
#         else:
#             # For interpreted languages
#             exec_cmd = config['command'].format(filename=filename)
#             exec_result = docker_client.containers.run(
#                 config['image'],
#                 exec_cmd,
#                 volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
#                 working_dir='/usr/src/app',
#                 network_disabled=True,
#                 mem_limit='100m',
#                 stderr=True,
#                 stdout=True,
#                 detach=False,
#                 remove=True,
#                 timeout=Config.EXECUTION_TIMEOUT
#             )
#             output = exec_result.decode()
#             return {'output': output}

#     except docker.errors.ContainerError as e:
#         return {'error': e.stderr.decode()}
#     except docker.errors.APIError as e:
#         return {'error': 'Docker API Error'}
#     except Exception as e:
#         return {'error': str(e)}
#     finally:
#         # Clean up temporary directory
#         try:
#             shutil.rmtree(temp_dir)
#         except Exception:
#             pass


# backend/api/execute.py

import docker
import uuid
import os
import tempfile
import shutil

from config import Config

docker_client = docker.from_env()

LANGUAGES = {
    'python': {
        'image': 'python:3.10-slim',
        'extension': '.py',
        'command': 'python {filename}'
    },
    'c': {
        'image': 'gcc:latest',
        'extension': '.c',
        'compile_command': 'gcc {filename} -o {output}',
        'execute_command': './{output}'
    },
    'java': {
        'image': 'openjdk:17-slim',
        'extension': '.java',
        'compile_command': 'javac {filename}',
        'execute_command': 'java {classname}'
    },
    'javascript': {
        'image': 'node:16-slim',
        'extension': '.js',
        'command': 'node {filename}'
    },
    # Add more languages as needed
}

def execute_code(language, code):
    if language not in LANGUAGES:
        return {'error': 'Unsupported language'}

    config = LANGUAGES[language]
    file_extension = config['extension']
    filename = f'Main{file_extension}'
    unique_id = str(uuid.uuid4())
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, filename)

    with open(file_path, 'w') as f:
        f.write(code)

    try:
        if language == 'c':
            # Compile C code
            compile_cmd = config['compile_command'].format(filename=filename, output='a.out')
            compile_result = docker_client.containers.run(
                config['image'],
                compile_cmd,
                volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
                working_dir='/usr/src/app',
                network_disabled=True,
                mem_limit='50m',
                stderr=True,
                stdout=True,
                detach=False,
                remove=True,
                timeout=Config.EXECUTION_TIMEOUT
            )
            if compile_result.decode().strip() != '':
                return {'error': compile_result.decode()}
            # Execute compiled C program
            exec_cmd = config['execute_command'].format(output='a.out')
            exec_result = docker_client.containers.run(
                config['image'],
                exec_cmd,
                volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
                working_dir='/usr/src/app',
                network_disabled=True,
                mem_limit='50m',
                stderr=True,
                stdout=True,
                detach=False,
                remove=True,
                timeout=Config.EXECUTION_TIMEOUT
            )
            output = exec_result.decode()
            return {'output': output}
        elif language == 'java':
            # Compile Java code
            classname = 'Main'
            compile_cmd = config['compile_command'].format(filename=filename)
            compile_result = docker_client.containers.run(
                config['image'],
                compile_cmd,
                volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
                working_dir='/usr/src/app',
                network_disabled=True,
                mem_limit='100m',
                stderr=True,
                stdout=True,
                detach=False,
                remove=True,
                timeout=Config.EXECUTION_TIMEOUT
            )
            if compile_result.decode().strip() != '':
                return {'error': compile_result.decode()}
            # Execute Java program
            exec_cmd = config['execute_command'].format(classname=classname)
            exec_result = docker_client.containers.run(
                config['image'],
                exec_cmd,
                volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
                working_dir='/usr/src/app',
                network_disabled=True,
                mem_limit='100m',
                stderr=True,
                stdout=True,
                detach=False,
                remove=True,
                timeout=Config.EXECUTION_TIMEOUT
            )
            output = exec_result.decode()
            return {'output': output}
        else:
            # For interpreted languages
            exec_cmd = config['command'].format(filename=filename)
            exec_result = docker_client.containers.run(
                config['image'],
                exec_cmd,
                volumes={temp_dir: {'bind': '/usr/src/app', 'mode': 'rw'}},
                working_dir='/usr/src/app',
                network_disabled=True,
                mem_limit='100m',
                stderr=True,
                stdout=True,
                detach=False,
                remove=True,
                timeout=Config.EXECUTION_TIMEOUT
            )
            output = exec_result.decode()
            return {'output': output}
    except docker.errors.ContainerError as e:
        return {'error': e.stderr.decode()}
    except docker.errors.APIError as e:
        return {'error': 'Docker API Error'}
    except Exception as e:
        return {'error': str(e)}
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
