Just set of scripts to initialise accpunt with production-like data:

# A - Basic Distributor Account Initialization
### INPUT
* Distributor Account Token
### ACTION(S)
* Create 2 Hubs with API type 
  - Production
  - Staging
* Create 2 Marketplaces with Icons, descriptions, currencies and price list attributes activated
  -  United States
  -  Germany
* Link Hubs with Marketplaces for Staging and Production environments
* Create Program Agreement
* Create Distribution Agreement for each Marketplace in the scope of the Program Agreement from the previous step
### OUTPUT
* Hub IDs
* Marketplace IDs
* Program Agreement ID

```bash
$ pip install -r requirements.txt
$ cd steps
$ python daccount.py 'distributor_account_token=ApiKey ...'
Hub created: HB-5446-4577 "Playground Hub 44566 - Staging"
Hub created: HB-7859-9984 "Playground Hub 63412 - Production"
Hub Marketplace: MP-18375 "Playground Marketplace 44566" for HB-5446-4577
Hub Marketplace: MP-59882 "Playground Marketplace 63412" for HB-7859-9984
Created Program Agreement AGP-777-708-207 Playground Program Agreement 5366
Created Distribution Agreement AGD-887-501-260 Distribution Playground Program Agreement 5366 for MP-18375
Created Distribution Agreement AGD-554-900-752 Distribution Playground Program Agreement 5366 for MP-59882
{
    "hubs": [
        "HB-5446-4577",
        "HB-7859-9984"
    ],
    "marketplaces": [
        "MP-18375",
        "MP-59882"
    ],
    "program_agreement_id": "AGP-777-708-207",
    "distribution_agreements": [
        "AGD-887-501-260",
        "AGD-554-900-752"
    ]
}
```