# oAPI (OpenAI API) PyLapi Generator Configuration

api_class_name = "oAPI"
output_py_name = "./oapi.py"
oas_file_name = "./openapi.yaml"

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

code_rewrite_file_name = "./oapi_rewrite.py"
