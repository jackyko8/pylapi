# Release Notes

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