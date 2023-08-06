__all__ = (
    'MMID1Type',
    'BaseMMID1',
    'create_uuid1',
    'create_uuid1_int',
)


from datetime import (
    datetime,
    timezone,
)
from decimal import (
    Decimal,
    ROUND_DOWN,
)
from random import getrandbits
from uuid import (
    RESERVED_NCS,
    RESERVED_MICROSOFT,
    RESERVED_FUTURE,
    RFC_4122,
    UUID,
    getnode,
    uuid1,
)
import typing

from chatora.util.marker import UNDEFINED
from chatora.mmid.constant import (
    EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX,
    MAX_CLOCK_SEQ,
    MASK_LOW_64_BITS,
    NODE_MASK,
    TSNS100_DECIMAL_EXP,
    TSUS_DECIMAL_EXP,
    UTC,
)
from chatora.mmid.base import BaseMMIDType


def create_uuid1(
    tsns: typing.Union[int, float, Decimal, None] = None,
    tsus: typing.Union[int, float, Decimal, None] = None,
    tsms: typing.Union[int, float, Decimal, None] = None,
    ts: typing.Union[int, float, Decimal, None] = None,
    dt: typing.Optional[datetime] = None,
    clock_seq: typing.Optional[int] = None,
    node: typing.Optional[int] = None,
) -> UUID:
    return UUID(int=create_uuid1_int(tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt, clock_seq=clock_seq, node=node))


def create_uuid1_int(
    tsns: typing.Union[int, float, Decimal, None] = None,
    tsus: typing.Union[int, float, Decimal, None] = None,
    tsms: typing.Union[int, float, Decimal, None] = None,
    ts: typing.Union[int, float, Decimal, None] = None,
    dt: typing.Optional[datetime] = None,
    clock_seq: typing.Optional[int] = None,
    node: typing.Optional[int] = None,
) -> int:
    if tsns is not None:
        uuid1_tsns100 = int(
            (tsns if isinstance(tsns, Decimal) else Decimal(str(tsns))) / 100
        ) + EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX
    elif tsus is not None:
        uuid1_tsns100 = int(tsus * 10) + EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX
    elif tsms is not None:
        uuid1_tsns100 = int(tsms * 10_000) + EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX
    elif ts is not None:
        uuid1_tsns100 = int(ts * 10_000_000) + EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX
    elif dt is not None:
        uuid1_tsns100 = int(dt.timestamp() * 10_000_000) + EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX
    else:
        raise ValueError('One of tsns, ts and dt MUST be set')

    if not 0 <= uuid1_tsns100 < (1 << 60):
        raise ValueError('timestamp is out of range')

    if clock_seq is None:
        clock_seq = getrandbits(14)
    elif not 0 <= clock_seq <= MAX_CLOCK_SEQ:
        raise ValueError('clock_seq is out of range')

    if node is not None:
        node = getnode()
    elif not 0 <= node < (1 << 48):
        raise ValueError('node is out of range')

    return (
        ((uuid1_tsns100 & 0xffff_ffff) << 96)
        | (((uuid1_tsns100 >> 32) & 0xffff) << 80)
        | (1 << 76)
        | (((uuid1_tsns100 >> 48) & 0xfff) << 64)
        | (0b10 << 62)
        | (clock_seq << 48)
        | node
    )


class MMID1Type(BaseMMIDType):

    def __init__(cls, name: str, bases: tuple, attr_map: dict):
        if hasattr(cls, 'TS_BIT_LENGTH') and hasattr(cls, 'EPOCH_DT'):
            if not 0 < cls.TS_BIT_LENGTH <= 55:
                raise ValueError('TS_BIT_LENGTH is out of range')
            elif cls.EPOCH_DT.tzinfo is None:
                raise ValueError('EPOCH_DT MUST be timezone aware.')
            cls.RESERVED_BIT_LENGTH = 55 - cls.TS_BIT_LENGTH
            cls.EPOCH_DT = cls.EPOCH_DT.astimezone(tz=UTC)
            cls.EPOCH_TS = cls.EPOCH_DT.timestamp()
            cls.EPOCH_TSMS = int(cls.EPOCH_TS * 1000)
            cls.EPOCH_TSUS = int(cls.EPOCH_TS * 1000_000)
            cls.EPOCH_TSNS = int(cls.EPOCH_TS * 1000_000_000)
            cls.EPOCH_TSNS100 = int(cls.EPOCH_TS * 10_000_000)
            cls.EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_MMID = cls.EPOCH_TSNS100 + EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX
            cls.MAX_TS_PART_VALUE = (1 << cls.TS_BIT_LENGTH) - 1
            cls.MAX_TSNS = cls.MAX_TS_PART_VALUE * 100 + cls.EPOCH_TSNS
            cls.MAX_DT = datetime.fromtimestamp(float(
                (Decimal(str(cls.MAX_TSNS)) / 1000_000_000).quantize(exp=TSUS_DECIMAL_EXP, rounding=ROUND_DOWN)
            ), tz=UTC,)
        super().__init__(name, bases, attr_map)
        return


class BaseMMID1(metaclass=MMID1Type):

    """
    https://www.percona.com/blog/2014/12/19/store-uuid-optimized-way/
    https://cjsavage.com/guides/mysql/insert-perf-uuid-vs-ordered-uuid-vs-int-pk.html
    https://gist.github.com/frsyuki/5513665

    UUID1:
    128  112  96   80   64   48   32   16
    LLLL-LLLL-MMMM-1HHH-sSSS-NNNN-NNNN-NNNN
        L: time_low
        M: time_mid
        1: UUID version 1
        H: time_high
        sSSS: clock_seq with variant
        sS: clock_seq_hi_variant
        SS: clock_seq_low
        NNNN-NNNN-NNNN: node

    MMID1v0 (55bit):
    128  112  96   80   64   48   32   16
    hHMM-MMLL-LLLL-1LLV-sSSS-NNNN-NNNN-NNNN
        hH: time_high with highest_bit
        M: time_mid
        L: time_low
        1: UUID version 1
        V: MMID version 1
        sSSS: clock_seq with variant
        sS: clock_seq_hi_variant
        SS: clock_seq_low
        NNNN-NNNN-NNNN: node
    """

    __slots__ = ('int',)
    # UUID_VERSION = 4
    # MMID_VERSION = 0
    HIGHEST_BIT = 0b1 << 127

    @classmethod
    def create_tsns100(
        cls,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
        default: typing.Any = UNDEFINED,
    ) -> int:
        if tsns is not None:
            return int(
                (tsns if isinstance(tsns, Decimal) else Decimal(str(tsns))) / 100
            ) - cls.EPOCH_TSNS100
        elif tsus is not None:
            return int(tsus * 10) - cls.EPOCH_TSNS100
        elif tsms is not None:
            return int(tsms * 10_000) - cls.EPOCH_TSNS100
        elif ts is not None:
            return int(ts * 10_000_000) - cls.EPOCH_TSNS100
        elif dt is not None:
            return int(dt.timestamp() * 10_000_000) - cls.EPOCH_TSNS100
        elif default is UNDEFINED:
            raise ValueError('No argument')
        else:
            return default

    @classmethod
    def create_int(
        cls,
        src_uuid1: typing.Optional[UUID] = None,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
        variant: typing.Optional[int] = None,
        clock_seq: typing.Optional[int] = None,
        node: typing.Optional[int] = None,
    ) -> int:
        mmid_tsns100 = cls.create_tsns100(tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt, default=None)
        if mmid_tsns100 is None or node is None:
            src_uuid1_int = uuid1().int if src_uuid1 is None else src_uuid1.int

        if mmid_tsns100 is None:
            mmid_tsns100 = (
               (((src_uuid1_int >> 64) & 0xfff) << 48)  # time_hi
               | (((src_uuid1_int >> 80) & 0xffff) << 32)  # time_mid
               | src_uuid1_int >> 96  # time_low
            ) - cls.EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_MMID
            if not 0 <= mmid_tsns100 <= cls.MAX_TS_PART_VALUE:
                raise ValueError('timestamp out of range')

            if variant is clock_seq is node is None:
                ts_value = mmid_tsns100 << cls.RESERVED_BIT_LENGTH
                return (
                    cls.HIGHEST_BIT
                    | ((ts_value >> 8) << 80)
                    | (cls.UUID_VERSION << 76)
                    | ((ts_value & 0xff) << 68)
                    | (cls.MMID_VERSION << 64)
                    | (src_uuid1_int & MASK_LOW_64_BITS)
                )
        elif not 0 <= mmid_tsns100 <= cls.MAX_TS_PART_VALUE:
            raise ValueError('timestamp out of range')

        if variant is None:
            variant = 0b10
        elif not 0 <= variant < (1 << 2):
            raise ValueError('variant out of range')

        if clock_seq is None:
            # Don't use generated uuid1 clock_seq.
            # clock_seq = (src_uuid1_int >> 48) & 0x3fff
            clock_seq = getrandbits(14)
        elif not 0 <= clock_seq <= MAX_CLOCK_SEQ:
            raise ValueError('clock_seq out of range')

        if node is None:
            node = src_uuid1_int & NODE_MASK
        elif not 0 <= node < (1 << 48):
            raise ValueError('node out of range')

        ts_value = mmid_tsns100 << cls.RESERVED_BIT_LENGTH
        return (
            cls.HIGHEST_BIT
            | ((ts_value >> 8) << 80)
            | (cls.UUID_VERSION << 76)
            | ((ts_value & 0xff) << 68)
            | (cls.MMID_VERSION << 64)
            | (variant << 62)
            | (clock_seq << 48)
            | node
        )

    @classmethod
    def create_min_int_from_time(
        cls,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
    ):
        return cls.create_int(tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt, variant=0, clock_seq=0, node=0)

    @classmethod
    def create_max_int_from_time(
        cls,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
    ):
        return cls.create_int(
            tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt, variant=0b11, clock_seq=MAX_CLOCK_SEQ, node=NODE_MASK,
        )

    @classmethod
    def create_min_instance_from_time(
        cls,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
    ):
        return cls(
            int_=cls.create_min_int_from_time(tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt),
        )

    @classmethod
    def create_max_instance_from_time(
        cls,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
    ):
        return cls(
            int_=cls.create_max_int_from_time(tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt),
        )

    def __init__(
        self,
        hex_: typing.Optional[str] = None,
        bytes_be: typing.Optional[bytes] = None,
        bytes_le: typing.Optional[bytes] = None,
        fields: typing.Optional[typing.Tuple[int, int, int, int, int, int]] = None,
        int_: typing.Optional[int] = None,
        check_required: bool = True,
        src_uuid1: typing.Optional[UUID] = None,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
        variant: typing.Optional[int] = None,
        clock_seq: typing.Optional[int] = None,
        node: typing.Optional[int] = None,
    ):
        if hex_ is bytes_be is bytes_le is fields is int_ is None:
            int_ = self.create_int(
                src_uuid1=src_uuid1, tsns=tsns, tsus=tsus, tsms=tsms, ts=ts, dt=dt,
                variant=variant, clock_seq=clock_seq, node=node,
            )
        elif hex_ is not None:
            int_ = int(hex_.replace('urn:', '').replace('uuid:', '').strip('{}').replace('-', ''), base=16)
        elif bytes_be is not None:
            int_ = int.from_bytes(bytes_be, byteorder='big')
        elif bytes_le is not None:
            int_ = int_.from_bytes(
                bytes_le[4 - 1::-1] + bytes_le[6 - 1:4 - 1:-1] + bytes_le[8 - 1:6 - 1:-1] + bytes_le[8:],
                byteorder='big',
            )
        elif fields is not None:
            (time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node) = fields
            if not 0 <= time_low < (1 << 32):
                raise ValueError('time_low out of range')
            if not 0 <= time_mid < (1 << 16):
                raise ValueError('time_mid out of range')
            if not 0 <= time_hi_version < (1 << 16):
                raise ValueError('time_hi_version out of range')
            if not 0 <= clock_seq_hi_variant < (1 << 8):
                raise ValueError('clock_seq_hi_variant out of range')
            if not 0 <= clock_seq_low < (1 << 8):
                raise ValueError('clock_seq_low out of range')
            if not 0 <= node < (1 << 48):
                raise ValueError('node out of range')

            mmid_tsns100 = (
               ((time_hi_version & 0xfff) << 48)
               | (time_mid << 32)
               | time_low
            ) - self.EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_MMID
            if not 0 <= mmid_tsns100 <= self.MAX_TS_PART_VALUE:
                raise ValueError('timestamp out of range')

            int_ = (
                self.HIGHEST_BIT
                | ((mmid_tsns100 >> 8) << 80)
                | (self.UUID_VERSION << 76)
                | ((mmid_tsns100 & 0xff) << 68)
                | (self.MMID_VERSION << 64)
                # force RFC4122 variant
                # | (((clock_seq_hi_variant & ~0xc0) | 0x80) << 56)  # with variant
                | (clock_seq_hi_variant << 56)  # with variant
                | (clock_seq_low << 48)
                | node
            )
            check_required = False

        if check_required is True:
            if not 0 <= int_ < (1 << 128):
                raise ValueError('out of range')
            elif (int_ >> 76) & 0xf != self.UUID_VERSION:
                raise ValueError(
                    f'UUID version `{(int_ >> 76) & 0xf}`'
                    f' does not match {self.__class__.__name__} version `{self.UUID_VERSION}`',
                )
            elif (int_ >> 64) & 0xf != self.MMID_VERSION:
                raise ValueError(
                    f'MMID_version `{(int_ >> 64) & 0xf}`'
                    f' does not match {self.__class__.__name__}.mmid_version `{self.MMID_VERSION}`',
                )
        self.int = int_
        return

    # def __setattr__(self, name, value):
    #     if name == 'int':
    #         return object.__setattr__(self, name, value)
    #     raise TypeError('UUID objects are immutable')

    def __eq__(self, other):
        if isinstance(other, BaseMMID1):
            return self.int == other.int
        elif isinstance(other, UUID):
            if other.version == 1:
                return (
                   self.time, self.int & MASK_LOW_64_BITS,
                ) == (
                    other.time, other.int & MASK_LOW_64_BITS,
                )
            else:
                return self.int == other.int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, BaseMMID1):
            return self.int < other.int
        elif isinstance(other, UUID):
            if other.version == 1:
                return (
                   self.time, self.int & MASK_LOW_64_BITS,
                ) < (
                    other.time, other.int & MASK_LOW_64_BITS,
                )
            else:
                return self.int < other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, BaseMMID1):
            return self.int > other.int
        elif isinstance(other, UUID):
            if other.version == 1:
                return (
                   self.time, self.int & MASK_LOW_64_BITS,
                ) > (
                    other.time, other.int & MASK_LOW_64_BITS,
                )
            else:
                return self.int > other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, BaseMMID1):
            return self.int <= other.int
        elif isinstance(other, UUID):
            if other.version == 1:
                return (
                   self.time, self.int & MASK_LOW_64_BITS,
                ) <= (
                    other.time, other.int & MASK_LOW_64_BITS,
                )
            else:
                return self.int <= other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, BaseMMID1):
            return self.int >= other.int
        elif isinstance(other, UUID):
            if other.version == 1:
                return (
                   self.time, self.int & MASK_LOW_64_BITS,
                ) >= (
                    other.time, other.int & MASK_LOW_64_BITS,
                )
            else:
                return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return f"{self.__class__.__name__}('{self}')"

    def __str__(self):
        h = f'{self.int:0>32x}'
        return f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}'

    @property
    def bytes(self) -> bytes:
        return self.int.to_bytes(16, 'big')

    @property
    def bytes_le(self) -> bytes:
        b = self.bytes
        return b[4-1::-1] + b[6-1:4-1:-1] + b[8-1:6-1:-1] + b[8:]

    @property
    def fields(self) -> typing.Tuple[int, int, int, int, int, int]:
        return (
            self.time_low, self.time_mid, self.time_hi_version,
            self.clock_seq_hi_variant, self.clock_seq_low, self.node
        )

    @property
    def time(self) -> int:
        v = (self.int & ~self.HIGHEST_BIT) >> 68
        return ((
            ((v >> 12) << 8)
            | (v & 0xff)
        ) >> self.RESERVED_BIT_LENGTH) + self.EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_MMID

    @property
    def time_low(self) -> int:
        return self.time & 0xffff_ffff

    @property
    def time_mid(self) -> int:
        return (self.time >> 32) & 0xffff

    @property
    def time_hi_version(self) -> int:
        return (
            (((self.int >> 76) & 0xf) << 12)
            | (self.time >> 48) & 0xfff
        )

    @property
    def time_hi_version1(self) -> int:
        return (
            (1 << 12)
            | (self.time >> 48) & 0xfff
        )

    @property
    def clock_seq_hi_variant(self) -> int:
        return (self.int >> 56) & 0xff

    @property
    def clock_seq_low(self) -> int:
        return (self.int >> 48) & 0xff

    @property
    def clock_seq(self) -> int:
        return (((self.clock_seq_hi_variant & 0x3f) << 8) |
                self.clock_seq_low)

    @property
    def node(self) -> int:
        return self.int & NODE_MASK

    @property
    def hex(self) -> str:
        return f'{self.int:0>32x}'

    @property
    def urn(self) -> str:
        return f'urn:uuid:{self}'

    @property
    def variant(self) -> str:
        validation_target = self.int >> 60
        if not validation_target & 0b1000:
            return RESERVED_NCS
        elif not validation_target & 0b0100:
            return RFC_4122
        elif not validation_target & 0b0010:
            return RESERVED_MICROSOFT
        else:
            return RESERVED_FUTURE
        # if not self.int & (0x8000 << 48):
        #     return RESERVED_NCS
        # elif not self.int & (0x4000 << 48):
        #     return RFC_4122
        # elif not self.int & (0x2000 << 48):
        #     return RESERVED_MICROSOFT
        # else:
        #     return RESERVED_FUTURE

    @property
    def version(self) -> int:
        # The version bits are only meaningful for RFC 4122 UUIDs.
        if self.variant == RFC_4122:
            return int((self.int >> 76) & 0xf)

    @property
    def timestamp_ns(self) -> int:
        return (self.time - EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX) * 100

    @property
    def timestamp_us(self) -> Decimal:
        return Decimal(self.time - EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX).quantize(
            exp=TSNS100_DECIMAL_EXP, rounding=ROUND_DOWN,
        ) / 10

    @property
    def timestamp_ms(self) -> Decimal:
        return Decimal(self.time - EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX).quantize(
            exp=TSNS100_DECIMAL_EXP, rounding=ROUND_DOWN,
        ) / 10_000

    @property
    def timestamp(self) -> float:
        return Decimal(self.time - EPOCH_TSNS100_DIFF_BETWEEN_UUID1_AND_UNIX).quantize(
            exp=TSNS100_DECIMAL_EXP, rounding=ROUND_DOWN,
        ) / 10_000_000

    @property
    def dt(self) -> datetime:
        return self.get_dt()

    @property
    def uuid1(self) -> UUID:
        t = self.time
        return UUID(
            int=(
                ((t & 0xffff_ffff) << 96)
                | (((t >> 32) & 0xffff) << 80)
                | (((1 << 12) | ((t >> 48) & 0xfff)) << 64)
                | (self.int & MASK_LOW_64_BITS)
            )
        )

    def get_dt(self, tzinfo: timezone = UTC) -> datetime:
        # Note that nanosecond-level precision is lost
        timestamp_us = self.timestamp_us
        s = int(timestamp_us / 1000_000)
        us = int(timestamp_us - s * 1000_000)
        if tzinfo is None:
            return datetime.utcfromtimestamp(s).replace(microsecond=us)
        else:
            return datetime.fromtimestamp(s, tz=tzinfo).replace(microsecond=us)

    def clone(
        self,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
        clock_seq: typing.Optional[int] = None,
        node: typing.Optional[int] = None,
    ) -> 'BaseMMID1':
        return self.__class__(
            int_=self.int if tsns is tsus is tsms is ts is dt is None else None,
            tsns=tsns, ts=ts, tsms=tsms, tsus=tsus, dt=dt,
            clock_seq=self.clock_seq if clock_seq is None else clock_seq,
            node=self.node if node is None else node,
        )

    def clone_as_uuid1(
        self,
        tsns: typing.Union[int, float, Decimal, None] = None,
        tsus: typing.Union[int, float, Decimal, None] = None,
        tsms: typing.Union[int, float, Decimal, None] = None,
        ts: typing.Union[int, float, Decimal, None] = None,
        dt: typing.Optional[datetime] = None,
        clock_seq: typing.Optional[int] = None,
        node: typing.Optional[int] = None,
    ) -> UUID:
        if tsns is tsus is tsms is ts is dt is clock_seq is node is None:
            return self.uuid1
        else:
            return UUID(int=create_uuid1_int(
                tsns=self.timestamp_ns if tsns is tsus is tsms is ts is dt is None else tsns,
                tsus=tsus, tsms=tsms, ts=ts, dt=dt,
                clock_seq=self.clock_seq if clock_seq is None else clock_seq,
                node=self.node if node is None else node,
            ))
