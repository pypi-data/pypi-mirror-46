

class BasePresentation(object):
    def __init__(self, context):
        self.context = context

    def present(self):
        pass


class ContextPresentation(object):
    def __init__(self, presentation):
        self.__presentation = presentation

    def do_present(self):
        return self.__presentation.present()