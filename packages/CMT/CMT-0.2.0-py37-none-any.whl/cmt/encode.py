from pathlib import Path
from typing import Union

from cmt.cmap.v0 import *
from cmt.cmap.v1 import *
from cmt.ecmap.v0 import *
from cmt.ecmap.v1 import *


def encode(source: Union[CMap_0, CMap_1, ECMap_0, ECMap_1], file: Path):
    with file.open("wb") as writer:
        writer.write(source.encode())
