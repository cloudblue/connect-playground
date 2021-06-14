import sys

sys.path.append('playground')
from playground import *

if __name__ == '__main__':
    try:
        ctx = Context.create(sys.argv[1:])
        ctx | DistributorAccountInitialization | VendorAccountCreation | Save

        print(ctx)
    except Exception as e:
        print(e)
