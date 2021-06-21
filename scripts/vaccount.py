
import random
import sys
from urllib.parse import urlsplit, parse_qs

from connect.cli.plugins.play.context import Context
from connect.cli.plugins.play.script import OptionWrapper, Script
from connect.cli.plugins.play.save import Save


class VendorAccountCreation(Script):
    """Create program contract, create vendor account."""

    @classmethod
    def options(cls):
        return [
            OptionWrapper('--distributor_account_token', help='Distributor account token'),
            OptionWrapper('--distributor_account_id', help='Distributor account ID (required only if token from user'),
            OptionWrapper('--program_agreement_id', help='Specify program agreement ID'),
        ]

    def select_context(self):
        if self.context.distributor_account_id and '@' in self.context.distributor_account_token:
            self.dclient.ns('auth').context.create({'account': {'id': self.context.distributor_account_id}})

    def create_program_contract(self):
        cid = random.randint(10000, 99999)
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
        self.program_contract = pc

    def create_vendor_account(self):
        activation_link = self.program_contract['activation']['link']
        print(f'Account activation Link is {activation_link}')
        code = parse_qs(urlsplit(activation_link).query)['secret'][0]
        users = self.dclient.users.all()
        vacc = self.dclient.accounts.create({
            'id': self.program_contract['partner']['id'],
            'name': self.program_contract['partner']['name'],
            'contract_id': self.context.program_contract_id,
            'code': code,
            'users': list(users),
        }, params=[('code', code)])

        print(f'Vendor Account created: {vacc["id"]} "{vacc["name"]}"')
        self.context.vendor_account_id = vacc['id']

    def create_vendor_account_token(self):
        # Switch context to vendor account
        self.dclient.ns('auth').context.create({'account': {'id': self.context.vendor_account_id}})

        t = self.dclient.ns('auth').tokens.create({
            'name': 'Playground token',
            'extension': {'id': 'EXT-000'},
            'description': 'This token to be used for manipulate for vendor playground staff'
        })

        full_token = f'ApiKey {t["id"]}:{t["token"]}'
        self.context.vendor_account_token = full_token
        print(f'Vendor token created: {t["id"]} "{t["name"]}" - {full_token}')

    def do(self, context=None):
        super().do(context=context)
        
        print('--- Vendor Account Creation ---')
        self.select_context()
        self.create_program_contract()
        self.create_vendor_account()
        self.create_vendor_account_token()


__all__ = ('VendorAccountCreation',)

if __name__ == '__main__':
    try:
        ctx = Context.create(sys.argv[1:])
        ctx | VendorAccountCreation | Save
        print(ctx)
    except Exception as e:
        print(e)
