from enum import EnumMeta

version = "0.2"


def _iter_str(cls):
    for x in cls._member_map_:
        yield x


_origin_contains = EnumMeta.__contains__


def _contains(cls, member):
    if isinstance(member, str):
        return member in cls._member_map_
    return _origin_contains(member)


def patch():
    EnumMeta.__contains__ = _contains
    EnumMeta.iter_str = _iter_str
