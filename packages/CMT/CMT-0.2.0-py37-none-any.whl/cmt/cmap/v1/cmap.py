import struct

from cmt import utils
from cmt.cmap.a_cmap import ACMap
from cmt.cmap.v1.checkpoint_times import CheckpointTimes
from cmt.cmap.v1.entity import Block, Dummy, PlayerStart, Sphere


class CMap(ACMap):
    """
    Celaria .cmap format (version 1)

    Datatypes:
    ===============================
    uByte > unsigned byte (1 byte)
    uShort > unsigned short (2 bytes)
    uInt > unsigned int (4 bytes)
    sShort > signed short (2 bytes)
    sInt > signed int (4 bytes)
    f32 > float (4 bytes)
    f64 > double (8 bytes)

    > <datatype> (<number of datatypes in sequence>) // <description>
    or
    > [<variable name>] : <datatype> (<number of datatypes in sequence>) // <description>

    ===============================

    > uByte (11) // string identifier
    > uByte (1) // version

    > nameLen : uByte (1) // number of characters in map name
    > uByte (nameLen) // map name as String

    > uByte (1) // boolean, previewCam_set

    > uByte (1) // number of checkpoint times (including finish line)

    > times : uByte (1) // number of checkpoint times (including finish line)

    > uInt (times) // checkpoint times for platin
    > uInt (times) // checkpoint times for gold
    > uInt (times) // checkpoint times for silver
    > uInt (times) // checkpoint times for bronze

    > f32 (1) // sun rotation on Z axis
    > f32 (1) // sun angle to xy plane (between 0 and 90 degrees)

    > f64 (1) // preview camera position x
    > f64 (1) // preview camera position y
    > f64 (1) // preview camera position z
    > f64 (1) // preview camera look at position x
    > f64 (1) // preview camera look at position y
    > f64 (1) // preview camera look at position z

    > entityNumber : uInt (1) // number of entities on the map

    for entity in entityNumber {
        > entityType : uInt (1) // entityType

        switch(entityType) {
            case 0: // block
                > blockType : uByte (1) // blockType/color
                > sInt (1) // position x
                > sInt (1) // position y
                > uInt (1) // position z
                > uInt (1) // scale x
                > uInt (1) // scale y
                > uInt (1) // scale z
                > f32 (1) // rotation on Z axis

                if (blockType == 5){ // checkpoint block
                    > uByte (1) // checkpoint Number
                }

            case 1: // sphere
                > sInt (1) // position x
                > sInt (1) // position y
                > uInt (1) // position z

            case 2: // player start
                > uByte (1) // unknown
                > sInt (1) // position x
                > sInt (1) // position y
                > uInt (1) // position z
                > f32 (1) // rotation on Z axis

            case 128: // dummy id
                > uByte (1) // ID
                > sInt (1) // position x
                > sInt (1) // position y
                > uInt (1) // position z
                > uInt (1) // scale x
                > uInt (1) // scale y
                > uInt (1) // scale z
                > f32 (1) // rotation on Z axis
        }
    }
    """

    def __init__(self):
        super().__init__(1)
        self.name = ""
        self.preview_cam_set = False
        self.checkpoint_times = None
        self.sun_rotation = 0.0
        self.sun_angle = 0.0
        self.camera_pos = (0.0, 0.0, 0.0)
        self.camera_look = (0.0, 0.0, 0.0)
        self.entities = []

    def __str__(self):
        return f"identifier: {self.identifier.name}\n" \
            f"format version: {self.format_version}\n" \
            f"name: {self.name}\n" \
            f"checkpoint times: {self.checkpoint_times}\n" \
            f"sun rotation: {self.sun_rotation}\n" \
            f"sun angle: {self.sun_angle}\n" \
            f"camera position: {self.camera_pos}\n" \
            f"camera look: {self.camera_look}\n" \
            f"entities: {len(self.entities)}"

    @classmethod
    def decode(cls, data: bytes, offset: int, debug: bool = False) -> 'CMAP':
        cmap = CMap()

        name_len = utils.unpack_from('<B', data, offset, ("name length",), debug)[0]
        offset += 1

        cmap.name = data[offset:offset + name_len].decode("utf-8")
        if debug:
            utils.debug_print(data[offset:offset + name_len], "name", cmap.name, offset)
        offset += name_len

        cmap.preview_cam_set = utils.unpack_from('<?', data, offset, ("preview cam set",), debug)[0]
        offset += 1

        # checkpoint times
        cmap.checkpoint_times = CheckpointTimes.decode(data, offset, debug)
        # checkpoint times count + checkpoint times * 4 (platin, gold, silver, bronze) * 4 bytes
        offset += 1 + 4 * len(cmap.checkpoint_times.platin) * 4

        cmap.sun_rotation = utils.unpack_from('<f', data, offset, ("sun rotation",), debug)[0]
        offset += 4

        cmap.sun_angle = utils.unpack_from('<f', data, offset, ("sun angle",), debug)[0]
        offset += 4

        cmap.camera_pos = utils.unpack_from('<ddd', data, offset, ("camera pos x", "camera pos y", "camera pos z"),
                                            debug)
        offset += 3 * 8

        cmap.camera_look = utils.unpack_from('<ddd', data, offset, ("camera look x", "camera look y", "camera look z"),
                                             debug)
        offset += 3 * 8

        # entities processing
        ent_count = utils.unpack_from('<I', data, offset, ("entity count",), debug)[0]
        offset += 4

        ent_done = 0
        while ent_done < ent_count:
            ent_type = utils.unpack_from('<B', data, offset, ("entity type",), debug)[0]
            offset += 1
            if ent_type == 0:
                cur_ent = Block.decode(data, offset, debug)
                cmap.entities.append(cur_ent)
                offset += cur_ent.byte_size
            elif ent_type == 1:
                cur_ent = Sphere.decode(data, offset, debug)
                cmap.entities.append(cur_ent)
                offset += cur_ent.byte_size
            elif ent_type == 2:
                cur_ent = PlayerStart.decode(data, offset, debug)
                cmap.entities.append(cur_ent)
                offset += cur_ent.byte_size
            elif ent_type == 128:
                cur_ent = Dummy.decode(data, offset, debug)
                cmap.entities.append(cur_ent)
                offset += cur_ent.byte_size
            else:
                raise ValueError(f"Unknown entity type: {ent_type} at {offset - 1}")
            ent_done += 1
        if debug:
            print(offset, " / ", len(data), " consumed")
        return cmap

    def encode(self) -> bytearray:
        data = bytearray()
        # file identifier
        data.extend(self.identifier.value.encode("utf-8"))
        # format version
        data.extend(struct.pack('<B', self.format_version))
        # length of name
        data.extend(struct.pack('<B', len(self.name)))
        # name
        data.extend(self.name.encode("utf-8"))
        # preview cam set
        data.extend(struct.pack('<?', self.preview_cam_set))
        # checkpoint times
        if self.checkpoint_times is not None:
            data.extend(struct.pack('<B', len(self.checkpoint_times.platin)))
            data.extend(self.checkpoint_times.encode())
        else:
            data.extend(struct.pack('<B', 0))
        # sun rotation
        data.extend(struct.pack('<f', self.sun_rotation))
        # sun angle
        data.extend(struct.pack('<f', self.sun_angle))
        # camera position
        data.extend(struct.pack('<ddd', *self.camera_pos))
        # camera look
        data.extend(struct.pack('<ddd', *self.camera_look))
        # entity count
        data.extend(struct.pack('<I', len(self.entities)))
        # entities
        for ent in self.entities:
            data.extend(ent.encode())
        return data
