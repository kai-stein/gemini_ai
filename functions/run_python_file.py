import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        #print(command)
        task_result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        #print(task_result.stdout)
        #print(task_result.stderr)
        #print(task_result.returncode)
        output = []
        if task_result.returncode != 0:
            output.append(f"Process exited with code {task_result.returncode}")
        if not task_result.stdout and not task_result.stderr:
            output.append("No output produced")
        if task_result.stdout:
            output.append(f"STDOUT:\n{task_result.stdout}")
        if task_result.stderr:
            output.append(f"STDERR:\n{task_result.stderr}")
        return "\n".join(output) 

    except Exception as e:
        return f'Error running file "{file_path}": {e}'
