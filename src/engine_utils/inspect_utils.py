import inspect


class InspectUtils:
    @staticmethod
    def has_init_param(clazz, param_name):
        if not hasattr(clazz, '__init__'):
            return False
        init_signature = inspect.signature(clazz.__init__)
        return param_name in init_signature.parameters
