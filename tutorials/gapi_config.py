# gAPI (GitHub API) PyLapi Generator Configuration

api_class_name = "gAPI"
output_py_name = "./gapi.py"
oas_file_name = "./api.github.com.json"

guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
    # "ref",
}

naming = {
    "class_name": "upperCamel($.path_segments[0]) + 'Resource'",
    "resource_name": "snake($.path_segments[0])",
    "class_path": "$.path_segments[0]",
    "resource_path": "'/'.join($.path_segments[1:])",
    "method_name": "lowerCamel($.operation_id)",
}

# code_rewrite_file_name = "./gapi_rewrite.py"
