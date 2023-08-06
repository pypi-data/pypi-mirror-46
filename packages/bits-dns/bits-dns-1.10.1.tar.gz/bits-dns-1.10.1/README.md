# bits-dns
BITS DNS Library

## Install

`pip install bits-dns`

## Use

```
from bits.dns import DNS
from bits.mhl import MHL

# initialize mhl
mhl = MHL()

# initialize dns
dns = DNS(mhl)

# get resource records
resource_records = dns.get_resource_records()

print('MHL Resource Records: %s' % (len(resource_records)))
```
