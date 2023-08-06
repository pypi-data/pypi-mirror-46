__all__ = (
    'EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX',
    'MASK_LOW_64_BITS',
    'MAX_CLOCK_SEQ',
    'NODE_MASK',
    'UTC',
    'TSNS_DECIMAL_EXP',
    'TSNS100_DECIMAL_EXP',
    'TSUS_DECIMAL_EXP',
    'TSMS_DECIMAL_EXP',
)

import datetime
import decimal


UTC = datetime.timezone.utc
MAX_CLOCK_SEQ: int = (1 << 14) - 1
NODE_MASK: int = 0xffffffffffff
MASK_LOW_64_BITS = 0xffff_ffff_ffff_ffff


# The number of 100-ns intervals between the
# UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX: int = 0x01b21dd213814000

# 4865183701896396700
#MMID1V0_MAX_TSNS = 0x7f_ffff_ffff_ffff * 100 + MMID1V0_EPOCH_TSNS
#MMID1V0_MAX_DT = datetime.datetime.fromtimestamp(
#    # 4865183701.896396
#    float((decimal.Decimal(MMID1V0_MAX_TSNS) / 1000_000_000).quantize(
#        exp=decimal.Decimal('0.000000'),
#        rounding=decimal.ROUND_DOWN,
#    )),
#    tz=datetime.timezone.utc,
#)


TSNS_DECIMAL_EXP = decimal.Decimal('0.000_000_001')
TSNS100_DECIMAL_EXP = decimal.Decimal('0.000_000_1')
TSUS_DECIMAL_EXP = decimal.Decimal('0.000_001')
TSMS_DECIMAL_EXP = decimal.Decimal('0.001')
