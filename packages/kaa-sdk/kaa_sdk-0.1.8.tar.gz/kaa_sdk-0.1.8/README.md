# Welcome to Kaa Python SDK

Current version of Kaa Python SDK covers authentication management and provides programmatic access for timeseries REST API.

# How to use
Step 1 - Set credentials

```
from kaa_sdk.config import set_credentials_file, set_config_file

set_credentials_file(uname='<YOUR_LOGIN>',
                     password='<YOUR_PASSWORD>',
                     client_id='<YOUR_CLIENT_ID>',
                     client_secret=<YOUR_CLIENT_SECRET>')
set_config_file(host='<KAA_HOST>',
                    auth_host='<KEYCLOAK_HOST>',
                    realm='<REALM>')
```
