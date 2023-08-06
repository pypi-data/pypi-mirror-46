from cerberus import Validator


class BaseValidation(object):
    def __init__(self, data, context={}):
        self.context = context
        self.__errors = None
        self.__data = data

    def validate(self):
        v = Validator(self.schema())

        if v.validate(self.__data):
            return True

        self.__errors = v.errors
        return False

    def get_errors(self):
        return self.__errors

    def get_data(self):
        return self.__data

    def schema(self):
        pass


class ContextValidation(object):

    def __init__(self, validation):
        self.__validation = validation

    def validate(self):
        return self.__validation.validate()

    @property
    def errors(self):
        return self.__validation.get_errors()

    @property
    def data(self):
        return self.__validation.get_data()

