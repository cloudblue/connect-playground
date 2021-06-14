
import random
import sys
from urllib.parse import urlsplit, parse_qs

from context import Context

from step import Step
from save import Save


class VendorAccountCreation(Step):
    def __init__(self, distributor_account_token=None, program_agreement_id=None):
        super().__init__()

        if distributor_account_token:
            self.context.distributor_account_token = distributor_account_token

        if program_agreement_id:
            self.context.program_agreement_id = program_agreement_id

    def create_program_contract(self):
        cid = random.randint(10000,99999)
        pc = self.dclient.agreements[self.context.program_agreement_id].contracts.create({
            'kind': 'production',
            'activation': {
                'message': f'Playground Contract {cid}',
            },
            'partner': {
                'name': f'Vendor for Playground contract {cid}'
            },
            'permissions': {
                'agreement': {
                    'program': {
                        'create': True,
                    },
                    'service': {
                        'create': False,
                        'delegate': False,
                    },
                },
            },
        })
        print(f'Program Contract created: {pc["id"]} "{pc["name"]}"')
        print(f'Partner created: {pc["partner"]["id"]} "{pc["partner"]["name"]}"')

        self.context.program_contract_id = pc['id']
        self.context.program_contract = pc

    def create_vendor_account(self):
        # Read from API
        pc = self.dclient.contracts[self.context.program_contract_id].get()
        activation_link = self.context.program_contract['activation']['link']
        print(f'Account activation Link is {activation_link}')
        code = parse_qs(urlsplit(activation_link).query)['secret'][0]
        users = self.dclient.users.all()
        vacc = self.dclient.accounts.create({
            'id': pc['partner']['id'],
            'name': pc['partner']['name'],
            'contract_id': self.context.program_contract_id,
            'code': code,
            'users': list(users),
        }, params=[('code', code)])

        print(f'Vendor Account created: {vacc["id"]} "{vacc["name"]}"')
        self.context.vendor_account_id = vacc['id']

    def create_vendor_account_token(self):
        t = self.dclient.ns('auth').tokens.create({
            'name': 'Playground token',
            'extension': {'id':'EXT-000'},
            'description': 'This token to be used for manipulate for vendor playground staff'
        })

        full_token = f'ApiKey {t["id"]}:{t["token"]}'
        self.context.vendor_accoint_token = full_token
        print(f'Vendor token created: {t["id"]} "{t["name"]}" - {full_token}')

    def do(self, context=None):
        super().do(context=context)

        self.create_program_contract()
        self.create_vendor_account()
        self.create_vendor_account_token()


if __name__ == '__main__':
    try:
        ctx = Context.create(sys.argv[1:])
        ctx | VendorAccountCreation | Save
        print(ctx)
    except Exception as e:
        print(e)
