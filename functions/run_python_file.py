import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
	
	fullpath = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
	abspath = os.path.abspath(working_directory)
	valid1 = os.path.commonpath([abspath, fullpath]) == abspath
	valid2 = os.path.isfile(fullpath)
	if valid1 is False:
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	elif valid2 is False:
		return f'Error: "{file_path}" does not exist or is not a regular file'
	elif not file_path.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file'
	else:
		try:
			command = ["python", fullpath]
			if args is not None:
				command.extend(args)
			process = subprocess.run(command, cwd=working_directory, capture_output=True,  timeout=30, text=True)
			returnString = f"STDOUT: {process.stdout}\nSTDERR: {process.stderr}"
			if not process.stdout and not process.stderr:
				returnString = "No output produced"
			if process.returncode != 0:
				returnString = returnString + f"\nProcess exited with code {process.returncode}"
			return returnString
		except Exception as e:
			return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the given Python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The relative path to the Python file to execute",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Set of arguments passed into the running file",
                },
            },
            "required": ["file_path"],
        },
    },
}
