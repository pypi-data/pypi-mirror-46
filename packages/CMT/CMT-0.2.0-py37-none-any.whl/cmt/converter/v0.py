from typing import Union

from cmt.a_converter import AConverter
from cmt.a_map import MapType
from cmt.cmap.v0 import *
from cmt.cmap.v1 import *
from cmt.ecmap.v0 import *
from cmt.ecmap.v1 import *


class Converter(AConverter):
    @staticmethod
    def convert_to(source: Union[CMap_0, ECMap_0], target: MapType) -> Union[CMap_0, ECMap_0]:
        if source.identifier == MapType.ECMAP and target == MapType.CMAP:
            return source.cmap
        elif source.identifier == MapType.CMAP and target == MapType.ECMAP:
            ecmap = ECMap_0()
            ecmap.cmap = source
            ecmap.cmap.medal_times = None
            return ecmap
        elif source.identifier == target:
            return source

        raise ValueError(
            f"Converting {source.identifier.name} {source.format_version} to {target.name} is not supported.")

    @staticmethod
    def downgrade(source: Union[CMap_0, ECMap_0]) -> None:
        raise ValueError(
            f"Downgrading {source.identifier.name} {source.format_version} to"
            f" {source.identifier.name} {source.format_version - 1} is not possible."
        )

    @staticmethod
    def upgrade(source: Union[CMap_0, ECMap_0]) -> Union[CMap_1, ECMap_1]:
        if source.identifier == MapType.CMAP:
            res = CMap_1()
            res.name = source.name

            if source.medal_times is not None:
                res.checkpoint_times = CheckpointTimes_1()
                # convert times, 60 ticks to 100 ticks
                for time in source.medal_times.platin:
                    res.checkpoint_times.platin.append(int(time * 5 / 3))
                for time in source.medal_times.gold:
                    res.checkpoint_times.gold.append(int(time * 5 / 3))
                for time in source.medal_times.silver:
                    res.checkpoint_times.silver.append(int(time * 5 / 3))
                for time in source.medal_times.bronze:
                    res.checkpoint_times.bronze.append(int(time * 5 / 3))

            res.sun_rotation = source.sun_rotation
            res.sun_angle = source.sun_angle
            res.camera_pos = source.camera_pos
            res.camera_look = source.camera_look

            for ent in source.entities:
                new_ent = None
                if type(ent) == Block_0:
                    new_ent = Block_1()
                    new_ent.block_type = ent.block_type
                    new_ent.position = ent.position
                    new_ent.scale = ent.scale
                    new_ent.rotation_z = ent.rotation_z
                    new_ent.checkpoint_nr = ent.checkpoint_nr
                    new_ent.byte_size = ent.byte_size
                elif type(ent) == Sphere_0:
                    new_ent = Sphere_1()
                    new_ent.position = ent.position
                elif type(ent) == PlayerStart_0:
                    new_ent = PlayerStart_1()
                    new_ent.position = ent.position
                    new_ent.rotation_z = ent.rotation_z
                elif type(ent) == Dummy_0:
                    new_ent = Dummy_1()
                    new_ent.id = ent.id
                    new_ent.position = ent.position
                    new_ent.scale = ent.scale
                    new_ent.rotation_z = ent.rotation_z
                if new_ent is not None:
                    res.entities.append(new_ent)
            return res
        elif source.identifier == MapType.ECMAP:
            res = ECMap_1()
            res.cmap = Converter.upgrade(source.cmap)
            return res
        raise ValueError(
            f"Upgrading {source.identifier.name} {source.format_version} to"
            f" {source.identifier.name} {source.format_version + 1} is not supported."
        )
