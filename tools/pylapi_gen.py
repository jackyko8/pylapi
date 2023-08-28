# PyLapi API Generator
#
# This script generates a PyLapi API from a configuration file.
#
# Steps:
# 1. Create a configuration file from the configuration template.
# 2. Customise the configuration file by following the insturctions in the comment.
# 3. Run this script with the configuration file as the first argument
#    - The OpenAPI specification JSON file is specified
#      - as the second argument, or if not specified
#      - in the configuration file `oas` variable, or if not specified
#      - as the configuration file name with .py replaced by .json
#    - The OpenAPI JSON file path is either absolute or relative to the current directory.

import json
import yaml
import re
import sys
import os
from getopt import getopt, GetoptError
from pylapi import PathDict
from pylapi import MagicWords

# Defaults
debug = False
oas_spec = {}
output_py = None
guide_attrs = None

# Default
all_guide_attrs = {
    "summary",
    "description",
    "parameters",
    "request_body",
}

control_guide_attrs = {
    "ref",
    "all",
}

valid_guide_attrs = all_guide_attrs.union(control_guide_attrs)

main_basename = os.path.basename(sys.argv[0])

# For naming conversion, use MagicWords(name).<conversion>, where <conversion> can be
# snake, kebab, pascal (upperCamel), camel (lowerCamel), or singular
# e.g., MagicWords("ThisIs a good_test for magic-words_conversion.").snake
#       Output: this_is_a_good_test_for_magic_words_conversion
def snake(phrase): return MagicWords(phrase).snake
def kebab(phrase): return MagicWords(phrase).kebab
def upperCamel(phrase): return MagicWords(phrase).upperCamel
def lowerCamel(phrase): return MagicWords(phrase).lowerCamel
def pascal(phrase): return MagicWords(phrase).pascal
def camel(phrase): return MagicWords(phrase).camel
def singular(phrase): return MagicWords(phrase).singular


class Method():
    def __init__(self, config, method):
        self.config = config
        self.method = method
        self.path_items = self.method["path"].split("/")

    def __repr__(self):
        return str(self.method)

    @property
    def api_path(self):
        _api_path = "/" + self.class_path if self.class_path else ""
        _api_path += "/" + self.resource_path if self.resource_path else ""
        return _api_path

    ########################################
    #
    # Derived attributes - customisables
    #   These attributes are derived from the original OpenAPI JSON
    #   attributes as described in the next section.
    #

    @property
    def class_name(self):
        # return MagicWords(MagicWords(self.path_items[0]).singular).upperCamel + "Resource"
        return eval(self.config.naming["class_name"].replace("$", "self"))

    # Resource Name used to create a resource object:
    # my_resource = MyAPI.resource("example_resource")
    # Example: Singular snake case for resource names
    @property
    def resource_name(self):
        # return MagicWords(MagicWords(self.path_items[0]).singular).snake
        return eval(self.config.naming["resource_name"].replace("$", "self"))

    # API path prefix for all methods in the class
    # API full path is {class_path}/{resource_path}
    # Example: resources in /resources/api_method/...
    # IMPORTANT: Make sure the class_path is common to all methods in the class.
    @property
    def class_path(self):
        # return self._path_items[0]
        # return ""
        return eval(self.config.naming["class_path"].replace("$", "self"))

    # API path suffix for the method
    # API full path is {class_path}/{resource_path}
    # Example: api_method in /resources/api_method/...
    @property
    def resource_path(self):
        # return "/".join(self._path_items[1:])
        # return "/".join(self.path_items)
        return eval(self.config.naming["resource_path"].replace("$", "self"))

    # Method Name
    # def exampleMethod(self):
    # Example: Lower Camel case for method names
    @property
    def method_name(self):
        # return MagicWords(self.operation_id).lowerCamel
        return eval(self.config.naming["method_name"].replace("$", "self"))


    ########################################
    #
    # Initialised attributes - not to be customised
    #   These attributes are captured from the
    #   OpenAPI JSON file, and returned without
    #   conversion (except http_method to uppercase).
    #
    @property
    def path(self):
        return self.method["path"]

    @property
    def http_method(self):
        return self.method["http_method"].upper()

    @property
    def operation_id(self):
        return self.method["operation_id"]

    # The followings are used for documentation in the generated file.
    # Comment out, or return blank, None, or False to suppress.
    @property
    def summary(self):
        return self.method["summary"]

    @property
    def description(self):
        return self.method["description"]

    @property
    def parameters(self):
        return self.method["parameters"]

    @property
    def request_body(self):
        return self.method["request_body"]


def usage(exit_code=0):
    print(f"""Usage: {main_basename} <config.py> [<openapi.json/yaml]
\t-h --help           Print this help message
\t-d --debug          Print all the methods to be generated then stop
\t-o --output=<file>  Output to <file> instead of stdout
\t-g --guide=<list>   Include some OpenAI attributes as comments; the list is comma-deliminted list with no spaces.
\t                    Valid attributes include: summary,description,parameters,request_body,all,ref
\t                    `all` means to include all items on the list
\t                    `ref` means to dereference $ref cells in OpenAI attributes""", file=sys.stderr)
    exit(exit_code)


def dict_checked(dict_data, attr, default=""):
    return dict_data[attr] if attr in dict_data else default


def printe(err):
    print(err, file=sys.stderr)


def printl(line=""):
    print(line.rstrip(), file=output_py)


def get_oas_spec(oas_file_name):
    _oas_spec = {}
    _oas_type = re.sub(r".+\.(json|yaml)$", "\\1", oas_file_name)

    try:
        if _oas_type == "json":
            _oas_spec = json.load(open(oas_file_name, "r"))
        elif _oas_type == "yaml":
            _oas_spec = yaml.safe_load(open(oas_file_name, "r"))
        else:
            raise Exception(f"Unknown OpenAI specification file type: {oas_file_name}")
    except:
        raise Exception(f"Cannot open OpenAI specification file: {oas_file_name}")

    for _ in ("openapi", "paths"):
        if _ not in _oas_spec:
            raise Exception(f'OpenAI Error: No "{_}" found in {oas_file_name}')

    return _oas_spec


def set_config(config, _oas_spec):
    # Get all config settings defined
    # Missing settings will be taken from _oas_spec

    # config.api_class_name fallback on oas.info.title
    try:
        api_class_name = config.api_class_name  # A trivial check
    except:
        try:
            api_class_name = _oas_spec["info"]["title"]
        except:
            raise Exception(f"API class name cannot be determined: Neither in config and nor in OpenAI specification")
        else:
            config.api_class_name = api_class_name

    # config.api_url fallback on oas.servers[0].url
    try:
        api_url = config.api_url  # A trivial check
    except:
        try:
            api_url = _oas_spec["servers"][0]["url"]
        except:
            raise Exception(f"API URL cannot be determined: Neither in config and nor in OpenAI specification")
        else:
            config.api_url = api_url


def get_methods(config, oas_paths):
    methods = []
    for oas_path in oas_paths:  # Loop through each API path in OAS
        oas_http_methods = oas_paths[oas_path]  # A list of HTTP methods, e.g., "get"
        if "parameters" in oas_http_methods:  # "parameters" is NOT an HTTP method
            del oas_http_methods["parameters"]
        for oas_http_method in oas_http_methods:  # Loop through each HTTP method the path supports
            oas_method = oas_http_methods[oas_http_method]  # A specification of the API method
            if "operationId" not in oas_method:
                raise Exception(f"operationId missing in {oas_path}:{oas_http_method}")
            # print(f"{oas_http_method.upper()} {oas_path}")
            # All attributes of `method_to_add` must be defined, even if not in OAS
            method_to_add = Method(config, {
                "path": oas_path.lstrip("/"),
                "http_method": oas_http_method,
                "operation_id": oas_method["operationId"],
                "summary": dict_checked(oas_method, "summary"),
                "description": dict_checked(oas_method, "description"),
                "parameters": [
                    {
                        _["name"]: {
                            "required": dict_checked(_, "required", False),
                            "in": dict_checked(_, "in"),
                            "description": dict_checked(_, "description"),
                        } for _ in oas_method["parameters"] if "name" in _
                    }
                ] if "parameters" in oas_method else [],
                "request_body": oas_method["requestBody"] if "requestBody" in oas_method else {},
            })

            # print(method_to_add)
            methods.append(method_to_add)

    methods.sort(key=lambda _: f"{_.class_name}/{_.method_name}")

    return methods


def gen_header(config, methods):
    # A set of unique class names
    class_set = sorted(set(_.class_name for _ in methods))
    classes = {}
    for class_name in class_set:
        # All methods in the class
        methods_of_class = [_.method_name for _ in methods if _.class_name == class_name]
        classes.update({
            class_name: {
                "methods": methods_of_class,
                "count": len(methods_of_class),
            }
        })

    printl(f"# PyLapi API generated by {main_basename}")
    printl(f"#")
    printl(f"# API Class: {config.api_class_name}")
    printl(f"# {len(classes)} Resource Classes (number of methods):")
    for _ in classes:
        printl(f"#      {_} ({classes[_]['count']})")
    printl(f"# Total: {len(methods)} methods")

    if debug:
        # Output OpenAI analysis then exit
        printl(f"#")
        ii = 0
        for method in methods:
            ii += 1
            printl(f"#{ii:4}. {method.class_name}:{method.method_name}(): {method.http_method} {method.path}")
        exit(0)

    return classes


def gen_api_class(config):

    printl("""
from pylapi import PyLapi, PyLapiError

class """+config.api_class_name+"""(PyLapi):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api_url = \""""+config.api_url+"""\"
        self.api_auth_type = \""""+config.api_auth_type+"""\"

        # Custom __init__ statements""")
    try:
        for init_line in config.api_class_init.split("\n"):
            printl(f"        {init_line}")
    except:
        pass
    printl()

    printl(f"    # Custom {config.api_class_name} methods")
    try:
        for api_method in config.api_methods.split("\n"):
            printl(f"    {api_method}")
    except:
        pass
    printl()


def print_class(config, method, classes):
        printl()
        printl(f"@{config.api_class_name}.resource_class(\"{method.resource_name}\", \"{method.class_path}\")")
        printl(f"class {method.class_name}({config.api_class_name}):")
        # printl()
        printl(f"# To instantiate: {config.api_class_name}.resource(\"{method.resource_name}\")")
        printl(f"# Number of methods: {classes[method.class_name]['count']}")
        for _ in classes[method.class_name]["methods"]:
            printl(f"#     {_}")


def print_method(config, method, resource_method_args_str):
    printl()
    printl(f"    @{config.api_class_name}.resource_method(\"{method.resource_path}\", http_method=\"{method.http_method}\"{resource_method_args_str})")
    printl(f"    def {method.method_name}(self): pass")
    # printl()
    printl(f"    # To call: {config.api_class_name}.resource(\"{method.resource_name}\").{method.method_name}(...)")
    printl(f"    # {method.http_method} {config.api_url}{method.api_path}")


def print_guide(method):
    def _multiline_trim(ml, n):
        _ml = ml
        _ml = re.sub(r"\n+$", "", _ml)
        _ml = re.sub(r"\n", "\n    #" + " " * n, _ml)
        _ml = re.sub(r" +\n", "\n", _ml)
        return _ml

    def _deref(data: dict, oas_spec: dict):
        if type(data) == dict:
            if len(data) != 1 or list(data.keys())[0] != "$ref":
                return {_: _deref(data[_], oas_spec) for _ in data}
            else:
                ref = data[list(data.keys())[0]]
                ref = re.sub(r"^#", "$", ref)
                ref = re.sub(r"/", ".", ref)
                return _deref(PathDict(oas_spec)[ref], oas_spec)
        elif type(data) == list:
            return [_deref(_, oas_spec) for _ in data]
        else:
            return data

    if "summary" in guide_attrs:
        try:
            summary = None
            if method.summary:
                summary = f"Summary: {method.summary}"
                summary = _multiline_trim(summary, 3)
        except:
            pass
        else:
            if summary != None:
                printl(f"    # {summary}")

    if "description" in guide_attrs:
        try:
            description = None
            if method.description:
                description = f"Description:\n{method.description}"
                description = _multiline_trim(description, 3)
        except:
            pass
        else:
            if description != None:
                printl(f"    # {description}")

    if "parameters" in guide_attrs:
        try:
            parameters = None
            if len(method.parameters) > 0 and method.parameters != [{}]:
                parameters = method.parameters.copy()
                if "ref" in guide_attrs:
                    parameters = _deref(parameters, oas_spec)
                parameters = "Parameters:\n" + re.sub(r"^-", " ", yaml.dump(parameters, indent=2, sort_keys=False))
                parameters = _multiline_trim(parameters, 1)
        except:
            pass
        else:
            if parameters != None:
                printl(f"    #")
                printl(f"    # {parameters}")

    if "request_body" in guide_attrs:
        try:
            rb_desc = None
            rb_content = None
            if method.request_body != {}:
                if "description" in method.request_body:
                    rb_desc = "  description: " + method.request_body['description']
                    rb_desc = _multiline_trim(rb_desc, 5)
                if "content" in method.request_body:
                    rb_content = method.request_body['content'].copy()
                    if "ref" in guide_attrs:
                        rb_content = _deref(rb_content, oas_spec)
                    rb_content = "  content:\n" + yaml.dump(rb_content, indent=2, sort_keys=False)
                    rb_content = _multiline_trim(rb_content, 5)
        except:
            pass
        else:
            if rb_desc != None or rb_content != None:
                printl(f"    #")
                printl(f"    # Request Body:")
                if rb_desc != None:
                    printl(f"    # {rb_desc}")
                if rb_content != None:
                    printl(f"    # {rb_content}")


def gen_resource_classes(config, methods, classes):
    resource_method_args_str = ""
    try:
        for resource_method_arg in config.resource_method_args:
            val = config.resource_method_args[resource_method_arg]
            if type(val) == str:
                val = f'"{val}"'
            resource_method_args_str += f", {resource_method_arg}={val}"
    except:
        pass

    # `resource_class` - change of first path item
    # `resource_method` - on every path, method being operation_id
    last_class_name = None
    num_methods = 0
    for method in methods:
        this_class_name = method.class_name
        if this_class_name != last_class_name:
            if last_class_name != None and num_methods == 0:
                printl("    pass")
                printl()
            last_class_name = this_class_name
            num_methods = 0
            print_class(config, method, classes)
        num_methods += 1
        print_method(config, method, resource_method_args_str)
        print_guide(method)
        printl()

    if last_class_name and num_methods == 0:
        printl("    pass")

    return resource_method_args_str


def main():
    global debug
    global output_py
    global oas_spec
    global guide_attrs

    ############################################################
    #
    # Arguments and configuration
    #

    # Getopt - cannot load config for defaults until after getopt
    try:
        opts, args = getopt(sys.argv[1:], "hdo:g:", ["help", "debug", "output=", "guide="])
    except GetoptError as err:
        printe(err)
        usage(2)

    for _o, _a in opts:
        if _o in ("-h", "--help"):
            usage()
        elif _o in ("-d", "--debug"):
            debug = True
        elif _o in ("-o", "--output"):
            output_py = open(_a, "w")
        elif _o in ("-g", "--guide"):
            guide_attrs = set(_a.split(","))
            unknown_specs = []
            for _ in guide_attrs:
                if _ not in valid_guide_attrs:
                    unknown_specs.append(_)
            if unknown_specs != []:
                printe(f"Unknown guide options: {', '.join(unknown_specs)}")
                usage(2)
            if "all" in guide_attrs:
                # Cannot copy over guide_attrs as "ref" may be in
                guide_attrs = guide_attrs.union(all_guide_attrs)
                guide_attrs.remove("all")
        else:
            printe("Invalid option: {_o}")
            usage(2)

    if len(args) < 1 or len(args) > 2:
        usage(1)

    config_file = args[0]

    config_module_name = re.sub(r"\.py$", "", os.path.basename(config_file))
    sys.path.append(os.path.dirname(config_file))
    import importlib
    config = importlib.import_module(config_module_name)

    oas_file_name = f"{config_module_name}.json"  # Default OpenAI definition
    if len(args) >= 2:
        # openapi.json specified
        oas_file_name = args[0]
    else:
        try:
            # Use config.oas if defined
            oas_file_name = config.oas_file_name
        except:
            # Use default
            pass

    if output_py == None:
        try:
            output_py = open(config.output_py_name, "w")
        except:
            output_py = sys.stdout

    if guide_attrs == None:
        try:
            guide_attrs = config.guide_attrs
        except:
            guide_attrs = set()


    ############################################################
    #
    # Generate the API SDK
    #

    oas_spec = get_oas_spec(oas_file_name)
    set_config(config, oas_spec)
    methods = get_methods(config, oas_spec["paths"])
    classes = gen_header(config, methods)
    gen_api_class(config)
    gen_resource_classes(config, methods, classes)


if __name__ == "__main__":
    main()
