import os

def get_file_content(working_directory: str, file_path: str) -> str:
	fullpath = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
	abspath = os.path.abspath(working_directory)
	valid1 = os.path.commonpath([abspath, fullpath]) == abspath
	valid2 = os.path.isfile(fullpath)
	if valid1 is False:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	elif valid2 is False:
		return f'Error: File not found or is not a regular file: "{file_path}"'
	else:
		try:
			with open(fullpath, "r") as f:
				file = f.read(10000)
				if f.read(1):
					file += f'[...File "{file_path}" truncated at 10000 characters]'
				return str(file)
		except Exception as e:
			return f"Error encountered: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the written contents of a given file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative file path containing the file to be read",
                },
            },
            "required": ["file_path"],
        },
    },
}
