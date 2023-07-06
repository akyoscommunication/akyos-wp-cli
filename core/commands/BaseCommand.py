class BaseCommand:

    def invoke(self, app, console):
        raise NotImplementedError("invoke() must be implemented in subclass")