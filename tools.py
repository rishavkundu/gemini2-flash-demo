def load_file_content(filename):
    try:
      with open(filename, "rt") as f:
          return {
              "result": f.read()
          }
    except Exception as e:
      return {
          "error": "Could not load file content",
      }

FUNCTIONS = {"load_file_content": load_file_content}

load_file_content_schema = {
    "name": "load_file_content",
    "description": "Summarize the text content of a file",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The name of the file",
            },
        },
        "required": ["filename"],
    },
    "output": {
        "type": "string",
        "description": "The text content of the file",
    },
}

tools_definitions = [
    {"function_declarations": [load_file_content_schema]}
]