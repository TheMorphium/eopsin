from eopsin.prelude import *


def compare(a: int, b: int) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    if a < b:
        return 1
    elif a == b:
        return 0
    else:
        return -1


def compare_extended_helper(time: ExtendedPOSIXTime) -> int:
    result = 0
    if isinstance(time, NegInfPOSIXTime):
        result = -1
    elif isinstance(time, FinitePOSIXTime):
        result = 0
    elif isinstance(time, PosInfPOSIXTime):
        result = 1
    return result


def compare_extended(a: ExtendedPOSIXTime, b: ExtendedPOSIXTime) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    a_val = compare_extended_helper(a)
    b_val = compare_extended_helper(b)
    if a_val != 0 or b_val != 0:
        return compare(a_val, b_val)
    a_finite: FinitePOSIXTime = a
    b_finite: FinitePOSIXTime = b
    return compare(a_finite.time, b_finite.time)


def get_bool(b: BoolData) -> bool:
    return isinstance(b, TrueData)


def compare_upper_bound(a: UpperBoundPOSIXTime, b: UpperBoundPOSIXTime) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    result = compare_extended(a.limit, b.limit)
    if result == 0:
        a_val = 1 if get_bool(a.closed) else 0
        b_val = 1 if get_bool(b.closed) else 0
        result = compare(a_val, b_val)
    return result


def compare_lower_bound(a: LowerBoundPOSIXTime, b: LowerBoundPOSIXTime) -> int:
    # a < b: 1
    # a == b: 0
    # a > b: -1
    result = compare_extended(a.limit, b.limit)
    if result == 0:
        a_val = 1 if get_bool(a.closed) else 0
        b_val = 1 if get_bool(b.closed) else 0
        result = compare(b_val, a_val)
    return result


def contains(a: POSIXTimeRange, b: POSIXTimeRange) -> bool:
    # Returns True if the interval `b` is entirely contained in `a`.
    lower = compare_lower_bound(a.lower_bound, b.lower_bound)
    upper = compare_upper_bound(a.upper_bound, b.upper_bound)
    return lower in [1, 0] and upper in [0, -1]


def make_range(
    lower_bound: POSIXTime,
    upper_bound: POSIXTime,
    lower_closed: BoolData,
    upper_closed: BoolData,
) -> POSIXTimeRange:
    return POSIXTimeRange(
        LowerBoundPOSIXTime(FinitePOSIXTime(lower_bound), lower_closed),
        UpperBoundPOSIXTime(FinitePOSIXTime(upper_bound), upper_closed),
    )


def make_from(lower_bound: POSIXTime, lower_closed: BoolData) -> POSIXTimeRange:
    return POSIXTimeRange(
        LowerBoundPOSIXTime(FinitePOSIXTime(lower_bound), lower_closed),
        UpperBoundPOSIXTime(PosInfPOSIXTime(), TrueData()),
    )


def make_to(upper_bound: POSIXTime, upper_closed: BoolData) -> POSIXTimeRange:
    return POSIXTimeRange(
        LowerBoundPOSIXTime(NegInfPOSIXTime(), TrueData()),
        UpperBoundPOSIXTime(FinitePOSIXTime(upper_bound), upper_closed),
    )
