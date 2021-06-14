from context import Context

from step import Step


class Save(Step):
    def do(self, filename=Context.context_file_name, context=None):
        super().do(context=context)
        self.context.save(filename=filename)
