__all__ = (
    'MMIDLoader',
)

import typing

from chatora.mmid.base import BaseMMIDType


class MMIDLoader:

    def __init__(
        self,
        factory_choice_map: typing.Optional[typing.Mapping[
            typing.Tuple[int, int], typing.Callable[[int, bool], BaseMMIDType]
        ]] = None,
    ):
        self.factory_choice_map = factory_choice_map or {}
        return

    def __call__(
        self,
        hex_value: str = None,
        bytes_be_value: bytes = None,
        bytes_le_value: bytes = None,
        int_value: int = None,
    ) -> BaseMMIDType:
        if hex_value is not None:
            int_value = int(hex_value.replace('urn:', '').replace('uuid:', '').strip('{}').replace('-', ''), base=16)
        elif bytes_le_value is not None:
            int_value = int.from_bytes(
                bytes_le_value[4 - 1::-1] + bytes_le_value[6 - 1:4 - 1:-1] + bytes_le_value[8 - 1:6 - 1:-1] + bytes_le_value[8:],
                byteorder='big',
            )
        elif bytes_be_value is not None:
            int_value = int.from_bytes(bytes_be_value, byteorder='big')

        if not 0 <= int_value < (1 << 128):
            raise ValueError('out of range')

        try:
            factory = self.resolve_factory(
                uuid_version=(int_value >> 76) & 0xf,
                mmid_version=(int_value >> 64) & 0xf,
            )
        except ValueError:
            raise ValueError(
                f'Unknown MMID `{int_value}`'
            )

        return factory(int_value, False)

    def register_factory(
        self,
        uuid_version: int,
        mmid_version: int,
        factory: typing.Callable[[int, bool], BaseMMIDType],
    ):
        self.factory_choice_map[(uuid_version, mmid_version)] = factory
        return

    def resolve_factory(self, uuid_version: int, mmid_version: int) -> typing.Callable[[int, bool], BaseMMIDType]:
        try:
            return self.factory_choice_map[(uuid_version, mmid_version)]
        except KeyError:
            raise ValueError(
                f'Unknown MMID type (uuid_version=`{uuid_version}`, mmid_version={mmid_version})'
            )
