import json

class Context(dict):
    @classmethod
    def create_by_args(cls, args):
        data = {}
        for k, v in [ a.split('=') for a in args ]:
            data[k] = v

        return cls(data)

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
        step.do(context=self)
        return self
