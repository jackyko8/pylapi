class aAPI(PyLapi):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api_url = "https://app.asana.com/api/1.0"
        self._resource_attrs.update({"gid": "$.gid"})

    @PyLapi.resource_method(give="$.data")
    def list(self): pass

    @PyLapi.resource_method(method_route="{gid}", give="$.data", load="$.data")
    def load(self): pass

    @PyLapi.resource_method(method_route="{gid}", http_method="PUT", send={"data": "$"}, give="$.data", load="$.data")
    def update(self): pass

    @PyLapi.resource_method(http_method="POST", send={"data": "$"}, give="$.data", load="$.data")
    def create(self): pass

    @PyLapi.resource_method(method_route="{gid}", http_method="DELETE", give=None)
    def delete(self): pass