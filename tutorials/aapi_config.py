# aAPI (Asana API) PyLapi Generator Configuration

api_class_name = "aAPI"
output_py_name = "./aapi.py"
oas_file_name = "./asana_oas.json"

guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
    # "ref",
}

naming = {
    "class_name": "upperCamel(singular($.path_segments[0])) + 'Resource'",
    "resource_name": "snake(singular($.path_segments[0]))",
    "class_path": "$.path_segments[0]",
    "resource_path": "re.sub(r'{[a-zA-Z0-9_-]+gid}', '{gid}', '/'.join($.path_segments[1:]))",
    "method_name": "lowerCamel($.operation_id)",
}

resource_class_args = {"gid": "$.gid"}

resource_method_args = {"send": {"data": "$"}, "give": "$.data"}

code_rewrite_file_name = "./aapi_rewrite.py"
