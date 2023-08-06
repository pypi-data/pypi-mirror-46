chatora.mmid
============

Python helper libraries for MMID which is similar to UUIDv1 but sortable.


## Usage
```python
import datetime
import random
import uuid
from chatora.mmid.api import BaseMMID1


BASE_DT = datetime.datetime(2011, 1, 1, tzinfo=datetime.timezone.utc)


class MMID1v0(BaseMMID1):
    __slots__ = ('int',)
    UUID_VERSION = 4
    MMID_VERSION = 0
    TS_BIT_LENGTH = 55
    EPOCH_DT = datetime.datetime(2010, 1, 1, tzinfo=datetime.timezone.utc)


# Construct
assert MMID1v0().version == 4
assert MMID1v0(dt=BASE_DT).dt == MMID1v0(ts=BASE_DT.timestamp()).dt == BASE_DT


# Sortable, which is useful for RDB column index (PostgreSQL UUID/BYTEA, MySQL BINARY).
assert MMID1v0(dt=BASE_DT) < MMID1v0(dt=BASE_DT + datetime.timedelta(days=1))

clock_seq = random.getrandbits(14)
assert MMID1v0(dt=BASE_DT, clock_seq=clock_seq) == MMID1v0(dt=BASE_DT, clock_seq=clock_seq)

# create_min_instance_from_time()/create_max_instance_from_time() may be useful in case of range query on RDB.
assert MMID1v0.create_min_instance_from_time(
    dt=BASE_DT,
) == MMID1v0(hex_='811ed178-c6c0-4000-0000-000000000000')

assert MMID1v0.create_max_instance_from_time(
    dt=BASE_DT,
) == MMID1v0(hex_='811ed178-c6c0-4000-ffff-ffffffffffff')



# Compatible with UUID1
uuid1 = uuid.uuid1()
mmid1v0 = MMID1v0(src_uuid1=uuid1)

assert uuid1 == mmid1v0
assert mmid1v0.uuid1 == uuid1
```
