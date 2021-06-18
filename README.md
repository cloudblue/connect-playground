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
$ ccli play
Reading scripts library from /home/user/scripts
Usage: ccli play [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  all                       Initialize everything that possible.
  init-distributor-account  Initialize distributor account.
  vendor-account-creation   Create program contract, create vendor account.
  
$ ccli play init-distributor-account --help
Reading scripts library from /home/user/scripts
Usage: ccli play init-distributor-account [OPTIONS]

Options:
  --distributor_account_token TEXT
                                  Distributor account token
  -h, --help                      Show this message and exit.

$ ccli play init-distributor-account
Reading scripts library from /home/user/scripts
--- Init Distributor Account ---
Hub created: HB-5446-4577 "Playground Hub 44566 - Staging"
Hub created: HB-7859-9984 "Playground Hub 63412 - Production"
Hub Marketplace: MP-18375 "Playground Marketplace 44566" for HB-5446-4577
Hub Marketplace: MP-59882 "Playground Marketplace 63412" for HB-7859-9984
Created Program Agreement AGP-777-708-207 Playground Program Agreement 5366
Created Distribution Agreement AGD-887-501-260 Distribution Playground Program Agreement 5366 for MP-18375
Created Distribution Agreement AGD-554-900-752 Distribution Playground Program Agreement 5366 for MP-59882
Saving context into context.json
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

# B - Vendor Account Creation
### INPUT
* Distributor Account Token
* Program Agreement ID
### ACTION(S)
* Create Program Contract based on the Input
# OUTPUT
* Program Contract ID
* Vendor Account ID
* Vendor Account Token

```bash
$ ccli play vendor-account-creation --help

Reading scripts library from /home/user/scripts
Usage: ccli play vendor-account-creation [OPTIONS]

Options:
  --program_agreement_id TEXT     Specify program agreement ID
  --distributor_account_token TEXT
                                  Distributor account token
  -h, --help                      Show this message and exit.
  
$ ccli play vendor-account-creation 
Loading context from context.json
--- Vendor Account Creation ---
Program Contract created: CRP-40536-98496-31778 "Contract of Playground Program Agreement 4162"
Partner created: VA-502-744 "Vendor for Playground contract 71501"
Account activation Link is https://portal.cnct.info/contracts/activate?secret=...
Vendor Account created: VA-502-744 "Vendor for Playground contract 71501"
Vendor token created: SU-903-473-071 "Playground token" - ApiKey SU-903-473-071:...
Saving context into context.json
```
