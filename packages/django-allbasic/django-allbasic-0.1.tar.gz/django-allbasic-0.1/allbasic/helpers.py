import json
from copy import deepcopy


class BaseHelper(object):

    def __init__(self, context):
        self.context = context

    def helpme(self):
        pass


class ContextHelper(object):

    def __init__(self, helper):
        self.__helper = helper

    def do_helpme(self):
        return self.__helper.helpme()


class HelperRequestData(BaseHelper):
    def helpme(self):
        request = self.context.get('request')
        return json.loads(request.data.decode('utf-8'))