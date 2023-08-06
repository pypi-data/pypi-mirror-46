from abc import abstractmethod, abstractclassmethod
from tfchain.encoders import BaseRivineObjectEncoder, BaseSiaObjectEncoder


class BaseDataTypeClass(BaseSiaObjectEncoder, BaseRivineObjectEncoder):
    """
    Base type defines the type all TFChain data types inheret from.
    """

    @abstractclassmethod
    def from_json(cls, obj):
        pass

    @abstractmethod
    def json(self):
        pass
