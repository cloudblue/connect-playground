import sys

from connect.cli.plugins.play.context import Context
from connect.cli.plugins.play.script import Script
from connect.cli.plugins.play.save import Save

from daccount import InitDistributorAccount
from vaccount import VendorAccountCreation


class InitAll(Script):
    """Initialize everything that possible."""

    @classmethod
    def command(cls):
        return 'all'

    def do(self, context=None):
        super().do(context=context)

        self.context | InitDistributorAccount | VendorAccountCreation


__all__ = ('InitAll',)

if __name__ == '__main__':
    try:
        ctx = Context.create(sys.argv[1:])
        ctx | InitAll | Save
        print(ctx)
    except Exception as e:
        print(e)
