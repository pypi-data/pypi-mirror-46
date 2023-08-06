import struct

from cmt import utils


class MedalTimes:
    def __init__(self):
        self.platin = []
        self.gold = []
        self.silver = []
        self.bronze = []

    def __str__(self):
        return f"platin: {self.platin} | gold: {self.gold} | silver: {self.silver} | bronze: {self.bronze}"

    @classmethod
    def decode(cls, data: bytes, offset: int, debug: bool = False) -> 'MedalTimes':
        m_times = MedalTimes()
        times = utils.unpack_from('<B', data, offset, ("medal times",), debug)[0]
        offset += 1
        # we do not use iter_unpack because its easier to use the offset debugging
        for i in range(times):
            m_times.platin.append(utils.unpack_from('<I', data, offset, ("platin time",), debug)[0])
            offset += 4

        for i in range(times):
            m_times.gold.append(utils.unpack_from('<I', data, offset, ("gold time",), debug)[0])
            offset += 4

        for i in range(times):
            m_times.silver.append(utils.unpack_from('<I', data, offset, ("silver time",), debug)[0])
            offset += 4

        for i in range(times):
            m_times.bronze.append(utils.unpack_from('<I', data, offset, ("bronze time",), debug)[0])
            offset += 4
        return m_times

    def encode(self) -> bytearray:
        """
        Excludes the length byte.
        :return:
        """
        data = bytearray()
        # medal platin
        for time in self.platin:
            data.extend(struct.pack('<I', time))
        # medal gold
        for time in self.gold:
            data.extend(struct.pack('<I', time))
        # medal silver
        for time in self.silver:
            data.extend(struct.pack('<I', time))
        # medal bronze
        for time in self.bronze:
            data.extend(struct.pack('<I', time))
        return data
