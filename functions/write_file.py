import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
	fullpath = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
	abspath = os.path.abspath(working_directory)
	valid1 = os.path.commonpath([abspath, fullpath]) == abspath
	valid2 = os.path.isdir(fullpath)
	if valid1 is False:
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	elif valid2 is True:
		return f'Error: Cannot write to "{file_path}" as it is a directory'
	else:
		try:
			parent = os.path.dirname(fullpath)
			os.makedirs(parent, exist_ok=True)
			with open(fullpath, "w") as f:
				f.write(content)
			return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
		except Exception as e:
			return f"Error encountered: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the given text content to a file at the specified path, overwriting it if it already exists",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative file path containing the file to be read",
                },
            "content": {
                "type": "string",
                "description": "The words to be written to the target file"
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
