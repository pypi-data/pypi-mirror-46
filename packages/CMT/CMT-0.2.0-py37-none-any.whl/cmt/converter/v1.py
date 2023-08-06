from typing import Union

from cmt.a_converter import AConverter
from cmt.a_map import MapType
from cmt.cmap.v0 import *
from cmt.cmap.v1 import *
from cmt.ecmap.v0 import *
from cmt.ecmap.v1 import *


class Converter(AConverter):
    @staticmethod
    def convert_to(source: Union[CMap_1, ECMap_1], target: MapType) -> Union[CMap_1, ECMap_1]:
        if source.identifier == MapType.ECMAP and target == MapType.CMAP:
            return source.cmap
        elif source.identifier == MapType.CMAP and target == MapType.ECMAP:
            ecmap = ECMap_1()
            ecmap.cmap = source
            ecmap.cmap.checkpoint_times = None
            return ecmap
        elif source.identifier == target:
            return source

        raise ValueError(
            f"Converting {source.identifier.name} {source.format_version} to {target.name} is not supported.")

    @staticmethod
    def downgrade(source: Union[CMap_1, ECMap_1]) -> Union[CMap_0, ECMap_0]:
        if source.identifier == MapType.CMAP:
            res = CMap_0()
            res.name = source.name

            if source.checkpoint_times is not None:
                res.medal_times = MedalTimes_0()
                # convert times, 100 ticks to 60 ticks
                for time in source.checkpoint_times.platin:
                    res.medal_times.platin.append(int(time * 0.6))
                for time in source.checkpoint_times.gold:
                    res.medal_times.gold.append(int(time * 0.6))
                for time in source.checkpoint_times.silver:
                    res.medal_times.silver.append(int(time * 0.6))
                for time in source.checkpoint_times.bronze:
                    res.medal_times.bronze.append(int(time * 0.6))

            res.sun_rotation = source.sun_rotation
            res.sun_angle = source.sun_angle
            res.camera_pos = source.camera_pos
            res.camera_look = source.camera_look

            for ent in source.entities:
                new_ent = None
                if type(ent) == Block_1:
                    new_ent = Block_0()
                    new_ent.block_type = ent.block_type
                    new_ent.position = ent.position
                    new_ent.scale = ent.scale
                    new_ent.rotation_z = ent.rotation_z
                    new_ent.checkpoint_nr = ent.checkpoint_nr
                    new_ent.byte_size = ent.byte_size
                elif type(ent) == Sphere_1:
                    new_ent = Sphere_0()
                    new_ent.position = ent.position
                elif type(ent) == PlayerStart_1:
                    new_ent = PlayerStart_0()
                    new_ent.position = ent.position
                    new_ent.rotation_z = ent.rotation_z
                elif type(ent) == Dummy_1:
                    new_ent = Dummy_0()
                    new_ent.id = ent.id
                    new_ent.position = ent.position
                    new_ent.scale = ent.scale
                    new_ent.rotation_z = ent.rotation_z
                if new_ent is not None:
                    res.entities.append(new_ent)
            return res
        elif source.identifier == MapType.ECMAP:
            res = ECMap_0()
            res.cmap = Converter.downgrade(source.cmap)
            return res
        raise ValueError(
            f"Downgrading {source.identifier.name} {source.format_version} to"
            f" {source.identifier.name} {source.format_version - 1} is not supported."
        )

    @staticmethod
    def upgrade(source: Union[CMap_1, ECMap_1]) -> Union['CMap_2', 'ECMap_2']:
        raise ValueError(
            f"Upgrading {source.identifier.name} {source.format_version} to"
            f" {source.identifier.name} {source.format_version + 1} is not supported."
        )
