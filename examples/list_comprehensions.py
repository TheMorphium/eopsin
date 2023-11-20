from eopsin.prelude import *


def validator(n: int, even: bool) -> List[int]:
    return (
        [k * k for k in range(n) if k % 2 == 0]
        if even
        else [k * k for k in range(n)]
    )
