from enum import EnumMeta

version = "0.3"


def _iter_name(cls):
    for x in cls._member_map_:
        yield x


def _iter_value(cls):
    for x in cls._member_map_.values():
        yield x.value


_origin_contains = EnumMeta.__contains__


def _contains(cls, member):
    if isinstance(member, str):
        return member in cls._member_map_
    return _origin_contains(cls, member)


def patch():
    EnumMeta.__contains__ = _contains
    EnumMeta.iter_name = _iter_name
    EnumMeta.iter_value = _iter_value
