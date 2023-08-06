import binascii
import codecs
import string

import collections
import numbers
from typing import Any

from typing import (
    Any,
    AnyStr
)


bytes_types = (bytes, bytearray)
integer_types = (int,)
text_types = (str,)
string_types = (bytes, str, bytearray)


def is_integer(value: Any) -> bool:
    return isinstance(value, integer_types) and not isinstance(value, bool)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes_types)


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


def is_boolean(value: Any) -> bool:
    return isinstance(value, bool)


def is_list_like(obj: Any) -> bool:
    return not is_string(obj) and isinstance(obj, collections.Sequence)


def is_list(obj: Any) -> bool:
    return isinstance(obj, list)


def is_tuple(obj: Any) -> bool:
    return isinstance(obj, tuple)


def is_dict(obj: Any) -> bool:
    return isinstance(obj, collections.Mapping)


def is_object(obj: Any) -> bool:
    return isinstance(obj, object)


def is_null(obj: Any) -> bool:
    return obj is None


def is_number(obj: Any) -> bool:
    return isinstance(obj, numbers.Number)


def is_text(value: Any) -> bool:
    return isinstance(value, text_types)


def decode_hex(value: str) -> bytes:
    if not is_text(value):
        raise TypeError("Value must be an instance of str")
    return codecs.decode(remove_0x_prefix(value), "hex")  # type: ignore


def encode_hex(value: AnyStr) -> str:
    if not is_string(value):
        raise TypeError("Value must be an instance of str or unicode")
    binary_hex = codecs.encode(value, "hex")  # type: ignore
    return add_0x_prefix(binary_hex.decode("ascii"))


def is_0x_prefixed(value: Any) -> bool:
    if not is_text(value):
        raise TypeError(
            "is_0x_prefixed requires text typed arguments. Got: {0}".format(repr(value))
        )
    return value.startswith("0x") or value.startswith("0X")


def remove_0x_prefix(value: str) -> str:
    if is_0x_prefixed(value):
        return value[2:]
    return value


def add_0x_prefix(value: str) -> str:
    if is_0x_prefixed(value):
        return value
    return "0x" + value

def is_hex(value: Any) -> bool:
    if not is_text(value):
        raise TypeError(
            "is_hex requires text typed arguments. Got: {0}".format(repr(value))
        )
    elif value.lower() == "0x":
        return True

    unprefixed_value = remove_0x_prefix(value)
    if len(unprefixed_value) % 2 != 0:
        value_to_decode = "0" + unprefixed_value
    else:
        value_to_decode = unprefixed_value

    if any(char not in string.hexdigits for char in value_to_decode):
        return False

    try:
        value_as_bytes = codecs.decode(value_to_decode, "hex")  # type: ignore
    except binascii.Error:
        return False
    except TypeError:
        return False
    else:
        return bool(value_as_bytes)