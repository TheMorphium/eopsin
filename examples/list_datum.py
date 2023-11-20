from eopsin.prelude import *


@dataclass()
class D2(PlutusData):
    list_field: List[DatumHash]


def validator(d: D2) -> bool:
    return d.list_field[0] == b"\x01"
