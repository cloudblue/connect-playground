
import random
import sys

from connect.cli.plugins.play.context import Context
from connect.cli.plugins.play.script import OptionWrapper, Script
from connect.cli.plugins.play.save import Save


class InitDistributorAccount(Script):
    """Initialize distributor account."""

    @classmethod
    def options(cls):
        return [
            OptionWrapper('--distributor_account_token', help='Distributor account token'),
        ]

    def create_hubs(self, extids):
        hubs = []

        for i, id in enumerate(extids):
            h = self.dclient.hubs.create({
                'name': f'Playground Hub {id} - {["Staging", "Production"][i]}',
                'description': f'Description for Playground Hub {id}',
                'instance': {
                    'id': f'playground-{id}',
                    'type': 'API',
                },
            })
            print(f'Hub created: {h["id"]} "{h["name"]}"')
            hubs.append(h["id"])

        self.context.hubs = hubs

    def create_marketplaces(self, extids):
        marketplaces = []

        for i, extid in enumerate(extids):
            hub_id = self.context['hubs'][i]
            m = self.dclient.marketplaces.create({
                'name': f'Playground Marketplace {extid}',
                'description': f'Description for Playground Marketplace {extid}',
                'countries': [{'id': ['US', 'DE'][i]}],
                'currency': ['USD', 'EUR'][i],
                'hubs': [{
                        'hub': {'id': hub_id},
                        'external_id': '1',
                }],
                'attributes': [{
                    'name': 'Suggested T0 Price',
                    'id': 'st0p',
                    'description': "Vendor's suggested Retail Customer (Tier-0) price, a.k.a. MSRP",
                }],
            })
            print(f'Hub Marketplace: {m["id"]} "{m["name"]}" for {hub_id}')
            marketplaces.append(m["id"])

        self.context.marketplaces = marketplaces

    def create_program_agreement(self):
        id = random.randint(1000, 9999)
        a = self.dclient.agreements.create({
            'title': f'Playground Program Agreement {id}',
            'description': f'Description Playground Program Agreement {id}',
            'type': 'program',
            'document_type': 'none',
            'active': True,
        })
        print(f'Created Program Agreement {a["id"]} {a["title"]}')

        self.context.program_agreement_id = a['id']
        self.program_agreement = a

    def create_distribution_agreements(self):
        self.context.distribution_agreements = []
        for mp_id in self.context.marketplaces:
            da = self.dclient.agreements[self.context.program_agreement_id].agreements.create({
                'type': 'distribution',
                'title': f'Distribution {self.program_agreement["title"]}',
                'description': f'Distribution {self.program_agreement["description"]}',
                'document_type': 'none',
                'active': True,
                'marketplace': {'id': mp_id},
                'auto_accept': True,
            })
            print(f'Created Distribution Agreement {da["id"]} {da["title"]} for {mp_id}')

            self.context |= ('distribution_agreements', da['id'])

    def do(self, context=None):
        super().do(context=context)

        print('--- Init Distributor Account ---')

        extids = [random.randint(10000, 99999) for _ in range(2)]
        self.create_hubs(extids)
        self.create_marketplaces(extids)
        self.create_program_agreement()
        self.create_distribution_agreements()


__all__ = ('InitDistributorAccount',)

if __name__ == '__main__':
    try:
        ctx = Context.create(sys.argv[1:])
        ctx | InitDistributorAccount | Save
        print(ctx)
    except Exception as e:
        print(e)
