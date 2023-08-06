from abc import ABC, abstractmethod

from cmt.a_map import AMap, MapType


class AConverter(ABC):
    @staticmethod
    @abstractmethod
    def convert_to(source: AMap, target: MapType):
        """
        Convert to the other map format of same version.
        :return:
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def downgrade(source: AMap):
        """
        Downgrade to the format version below.
        :return:
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def upgrade(source: AMap):
        """
        Upgrade to the format version above.
        :return:
        """
        raise NotImplementedError
