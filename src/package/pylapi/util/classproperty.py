# Acknowledgement: https://stackoverflow.com/questions/5189699/how-to-make-a-class-property

class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        # logger.debug(f"__init__({self}, {fget}. {fset})")
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        # logger.debug(f"__get__({self}, {obj}, {klass})")
        if klass is None:
            klass = type(obj)
        # logger.debug(f"self.fget.__get__({obj}, {klass})()")
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        # logger.debug(f"__set__({self}, {obj}, {value})")
        if not self.fset:
            raise AttributeError("Cannot set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        # logger.debug(f"setter({func})")
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self

def classproperty(func):
    # logger.debug(f"classproperty({func})")
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)
