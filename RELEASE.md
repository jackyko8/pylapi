# Release Notes

Version 0.12.4 2023-09-20
- Refactor MagicO out of AttrDict and PathDict, and put it into a separate project
- More typings with Union instead of Any
- Remove URL from .auth() - so no URL change
- Start user guide
- Put DeepLog back

Version 0.12.3 2023-09-16
- General
  - Rename "route" to "path"
- pylapi
  - Add .resource_data property
  - Add .raw_response property
- pylapi_gen
  - Check class name overlaps (resource consolidation)
  - Enhance error for giving the wrong config.py file in pylapi_gen
  - Enhance resource_method guide with keyword arguments from API path
  - Fix left-over classes in pylapi_gen
  - Add resource_class_args configuration
- PathDict
  - Add dict and list methods to PathDict to be in line with AttrDict
  - Fix PathDict bool assignment issue
    - fail when _value = False
    - use _value != None instead
- More tutorials

Version 0.12.2 2023-09-13
- Add README.md
- Rename path_items to path_segments
- pylapi_gen checks over-consolidation in class name (invalid_classes)
- Move OAS, config, and rewrite files to tutorial (instead of soft linking)
- More toturials

Version 0.12 2023-09-07
- Add auto resource attrs mapping based on method route
- Upload to PyPI test
- Update src/README.md
- Add PyLapi and root API class direct instantiation test
- Add upper camel case to oas.info.title as default api_class_name

Version 0.11 2023-09-06
- Code Rewrite in pylapi_gen
- Add more parameters guides
- Combine dotted_dict with path_dict
- Remove path_str from pylapi.py
- Convert AttrDict and PathDict to dict before rewrite
- Remove unnecessary util files and move the rest to be with pylapi.py
- Remove @classproperty as @property already covers this in Python 3.x (must use object, not class syntax in calls)
- Add recursive del_attr()
- Rename resource_ids to resource_attrs

Version 0.10 2023-08-28
- Move non-customisable code from pylapi_config_template.py to pylapi_gen.py
- Add more customisations into pylapi_config_template.py
- Generalise the config module location (not having to be with the gen script)

Version 0.9 2023-08-27
- Factorise pylapi_gen.py into functions
- Improve pylapi_gen.py: usage, getopt, guide_attrs, deref, request_body
- Add PyLapiError and allow_api_raise
- Rename common to util
- Standardise upper CamelCase for class names
- Recommend requirements.txt

Version 0.8 2023-08-25
- Rename package
- Tidy up directory structure

Version 0.7 2023-08-25
- Improve guided comments in generated SDK file
- Baseline before renaming

Version 0.6 2023-08-23
- Add gen_pylapi_sdk.py to generate SDKs from OpenAPI specifications
- Update examples to work with latest generated SDKs
- Add MagicWords for naming conversion in generator configuration
- Add pathDict to formalise dotted_dict
- Add comments in dotted_dict
- Add OpenAI conversation.py as a demo
- Reorganise and rename some files
- PyLapi tidy up logger.debug
- Add raw_request to return unwashed request attribute for callbacks
- Remove outdated comments

Version 0.5 2023-08-18
- Add resource method callbacks
- Fix resource method default assignments
- Data argument accepts "$..." with self._resource_data embedded using "$...".
- Take HTTPStatus 200-299 to be OK (instead of just 200)
- Overhall of class_method argument processing
- Rename resource_method `load_path` to `load` and `data_path` to `give`
- Add `send` to resource_method

Version 0.4 2023-08-09
- Concepture design
  - Rename most variables in pylapi.py to be consistent with the concepture design
  - Rename @api_method to @resource_method
  - Rename @api_class to @resource_class
  - Swap back argument order in @resource_class(resource_name, resource_route) and resource_route defaults to ""
- Bug fixing
  - Refine security (`_wash_auth`)
  - Fix resource method calls with positional arguments
  - Fix resource.data attribute
  - Make resource_ids and api_base_headers @property (instead of @classproperty)
    - relunctantly until finding a solution to make them @property
- Error handling
  - Add self.request, self.request_method, self.response, self.response_data
  - Add response_ok() to PyLapi (allowing resource classes to override)
  - Add class methods to handle log levels
  - Make resource methods a callback function (e.g., to change `self._response_data` if necessary), instead of code being ignored.
    - Will separate into `initially` and `finally` in the next release
- Documentation
  - Update sdk/README.md
  - More tutorials

Version 0.3 2023-08-07
- Enhance attrDict to include dict and list methods
- Streamline pylapi.py

Version 0.2 2023-08-07
- Wash auth token in all their display and headers
- Use auth() to auth, instead of assignment to api_auth
- Attribute Dict in resource_obj.data resolved by adding the attrDict class
- Argument order in @api_class(resource_route, resource_name) and resource_name default to resource_route
- Allow @api_method instead of requiring @api_method("")
- Add @classproperty
- api_url settable in API class
- Add response_ok() check in root class (so subclasses can overwrite it)
- More sample classes, example scripts and tutorial notebooks
- WIP: sdk/README.md

Version 0.1 2023-08-03
- First release
