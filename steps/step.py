from context import Context
from connect.client import ConnectClient


class Step:
    context: Context = None
    endpoint: str = None

    def __init__(self, context=None, **kwargs):
        self.context = context if context is not None else Context()
        self.context.update(kwargs)

    def client(self, token):
        return ConnectClient(token, endpoint=self.context['endpoint'], use_specs=False)

    def do(self, context=None):
        if context:
            context.update(self.context)
            self.context = context
