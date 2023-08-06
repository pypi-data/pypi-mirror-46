Planhat Python
==============

Planhat API Python client library

https://docs.planhat.com/

## Installation



## Usage

```python
from planhat import Planhat

# See https://docs.planhat.com/#base-url
from planhat import API_URL, API_URL_EU, API_URL_US2

# https://app.planhat.com/developer
planhat_client = Planhat(
    API_URL,
    'tenant-token',
    'api-token'
)

companies_data = planhat_client.get_companies()
```
