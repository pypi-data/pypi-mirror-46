from typing import Union

from cmt.a_converter import AConverter
from cmt.a_map import MapType
from cmt.cmap.v0 import *
from cmt.cmap.v1 import *
from cmt.converter import *
from cmt.ecmap.v0 import *
from cmt.ecmap.v1 import *


def _get_converter(version: int) -> AConverter:
    if version == 0:
        return Converter_0()
    elif version == 1:
        return Converter_1()
    raise ValueError(f"Converter for version {version} does not exist.")


def convert(source: Union[CMap_0, CMap_1, ECMap_0, ECMap_1], version: int, target: MapType) -> Union[
    CMap_0, CMap_1, ECMap_0, ECMap_1]:
    res = source
    while res.format_version != version:
        if res.format_version > version:
            res = _get_converter(res.format_version).downgrade(res)
        else:
            res = _get_converter(res.format_version).upgrade(res)

    if res.identifier != target:
        return _get_converter(res.format_version).convert_to(res, target)
    return res
