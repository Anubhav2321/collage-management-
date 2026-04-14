# students/compiler_service.py
import os
import uuid
import subprocess
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Directory to temporarily store student codes
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_codes')
os.makedirs(TEMP_DIR, exist_ok=True)

@csrf_exempt
def run_code_in_docker(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid Request'})
        
    try:
        data = json.loads(request.body)
        language = data.get('language', 'python')
        code = data.get('code', '')
        
        if not code.strip():
            return JsonResponse({'status': 'error', 'message': 'Code cannot be empty.'})

        # 1. Create a unique filename to prevent conflicts between students
        unique_id = str(uuid.uuid4())
        
        # Determine file extension and run command based on language
        if language == 'python':
            file_ext = '.py'
            run_cmd = ['python3', f'/app/{unique_id}{file_ext}']
        elif language == 'javascript':
            file_ext = '.js'
            run_cmd = ['node', f'/app/{unique_id}{file_ext}']
        elif language == 'cpp':
            file_ext = '.cpp'
            # C++ needs compilation first, then execution
            run_cmd = ['sh', '-c', f'g++ /app/{unique_id}{file_ext} -o /app/{unique_id} && /app/{unique_id}']
        elif language == 'java':
            file_ext = '.java'
            # For simplicity in this basic setup, we assume the class is named Main
            run_cmd = ['sh', '-c', f'javac /app/{unique_id}{file_ext} && cd /app && java Main']
        else:
            return JsonResponse({'status': 'error', 'message': 'Unsupported language.'})

        file_name = f"{unique_id}{file_ext}"
        file_path = os.path.join(TEMP_DIR, file_name)

        # 2. Save the code to the temporary file
        with open(file_path, 'w') as f:
            f.write(code)

        # 3. Build the Docker command
        # We mount (bind) the temp directory to /app inside the container
        docker_cmd = [
            'docker', 'run', '--rm', 
            '-v', f"{TEMP_DIR}:/app", # Share folder
            '--network', 'none',      # Security: No internet access for student code
            '--memory', '256m',       # Security: Limit memory
            '--cpus', '0.5',          # Security: Limit CPU
            'local-compiler'          # The image we built in Step 1
        ] + run_cmd

        # 4. Execute the command with a timeout (e.g., 5 seconds) to prevent infinite loops
        try:
            process = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            output = process.stdout
            error = process.stderr
            
            if process.returncode == 0:
                result_status = 'success'
                final_output = output if output else "Execution completed (No output)"
            else:
                result_status = 'error'
                final_output = error if error else output

        except subprocess.TimeoutExpired:
            result_status = 'error'
            final_output = "Timeout Error: Your code took too long to execute (Possible Infinite Loop)."
            
        finally:
            # 5. Cleanup: Always delete the temporary file after execution
            if os.path.exists(file_path):
                os.remove(file_path)
                
            # Note: For C++ and Java, compiled files (.class, executable) might remain in TEMP_DIR. 
            # In a production app, you'd clean those up too based on the unique_id.

        return JsonResponse({'status': result_status, 'output': final_output})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})