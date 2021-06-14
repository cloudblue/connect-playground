
import random
import sys

from context import Context
from step import Step
from connect.client import ConnectClient


class DistributorAccountInitialization(Step):
    created: dict
    client: ConnectClient

    def __init__(self, distributor_account_token=None):
        super().__init__()
        if distributor_account_token:
            self.context.distributor_account_token=distributor_account_token

    def create_hubs(self, extids):
        hubs = []

        for i, id in enumerate(extids):
            h = self.client.hubs.create({
                'name': f'Playground Hub {id} - {["Staging", "Production"][i]}',
                'description': f'Description for Playground Hub {id}',
                'instance': {
                    'id': f'playground-{id}',
                    'type': 'API',
                }
            })
            print(f'Hub created: {h["id"]} "{h["name"]}"')
            hubs.append(h["id"])

        self.context |= ('hubs', hubs)

    def create_marketplaces(self, extids):
        marketplaces = []

        for i, id in enumerate(extids):
            hub_id = self.context['hubs'][i]
            m = self.client.marketplaces.create({
                                        'name': f'Playground Marketplace {id}',
                                        'description': f'Description for Playground Marketplace {id}',
                                        'countries': [{'id': ['US', 'DE'][i]}],
                                        'currency': ['USD', 'EUR'][i],
                                        'hubs': [{
                                                'hub': { 'id': hub_id },
                                                'external_id': '1'
                                        }],
                                        'attributes':[{
                                                'name':'Suggested T0 Price',
                                                'id':'st0p',
                                                'description': "Vendor's (manufacturer's) suggested Retail Customer (Tier-0) price, a.k.a. MSRP."
                                        }]
            })
            print(f'Hub Marketplace: {m["id"]} "{m["name"]}" for {hub_id}')
            marketplaces.append(m["id"])

        self.context |= ('marketplaces', marketplaces)

    def create_program_agreement(self):
        id = random.randint(1000, 9999)
        a = self.client.agreements.create({
            'title': f'Playground Program Agreement {id}',
            'description': 'Description Playground Program Agreement {id}',
            'type': 'program',
            'document_type': 'none',
            'active': True,
        })
        print(f'Created Program Agreement {a["id"]} {a["title"]}')

        self.context.program_agreement_id = a['id']
        self.context.program_agreement = a

    def create_distribution_agreements(self):
        for mp_id in self.context.marketplaces:
            da = self.client.agreements[self.context.program_agreement_id].agreements.create({
                        'type': 'distribution',
                        'title': f'Distribution {self.context.program_agreement["title"]}',
                        'description': f'Distribution {self.context.program_agreement["description"]}',
                        'document_type': 'none',
                        'active': True,
                        'marketplace': {'id': mp_id},
                        'auto_accept': True,
            })
            print(f'Created Distribution Agreement {da["id"]} {da["title"]} for {mp_id}')

            self.context |= ('distribution_agreements', da['id'])

    def do(self, context=None):
        super().do(context=context)

        self.created = {}
        self.client = self.client(self.context.distributor_account_token)

        extids = [random.randint(10000, 99999) for _ in range(2)]
        self.create_hubs(extids)
        self.create_marketplaces(extids)
        self.create_program_agreement()
        self.create_distribution_agreements()


if __name__ == '__main__':
    ctx = Context.create_by_args(sys.argv[1:])
    ctx | DistributorAccountInitialization()
    print(ctx)
