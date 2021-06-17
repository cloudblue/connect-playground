import inspect
import json
import sys


class Context(dict):
    context_file_name = 'context.json'

    @classmethod
    def create_from_file(cls, filename=context_file_name):
        ctx = cls()
        try:
            ctx.load(filename)
        except FileNotFoundError:
            pass

        return ctx

    @classmethod
    def create(cls, args=None, filename=context_file_name):
        ctx = cls()
        try:
            ctx.load(filename)
        except FileNotFoundError:
            pass

        if args:
            ctx.parse_args(args)

        return ctx

    def parse_args(self, args):
        for k, v in [a.split('=') for a in args]:
            self[k] = v

    def load(self, filename=context_file_name):
        with open(filename) as f:
            print(f'Loading context from {filename}', file=sys.stderr)
            self.clear()
            for k, v in json.load(f).items():
                self[k] = v

    def save(self, filename=context_file_name):
        with open(filename, 'w') as f:
            print(f'Saving context into {filename}', file=sys.stderr)
            json.dump(self, f, indent=4)

    def __str__(self):
        return json.dumps(self, indent=4)

    def __getattr__(self, item):
        if item in self:
            return self[item]

        raise KeyError(item)

    def __setattr__(self, key, value):
        self[key] = value

    def __ior__(self, kv):
        key, value = kv
        if isinstance(value, dict):
            if key not in self:
                self[key] = {}
            self[key].update(key)
        else:
            if not isinstance(value, list):
                value = [value]

            if key not in self:
                self[key] = []

            self[key].extend(value)

        return self

    def __or__(self, step):
        if inspect.isclass(step):
            step = step()

        step.do(context=self)
        return self
