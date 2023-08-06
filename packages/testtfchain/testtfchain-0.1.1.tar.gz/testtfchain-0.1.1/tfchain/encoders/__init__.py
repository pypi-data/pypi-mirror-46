from tfchain.encoders.rivine import RivineBinaryObjectEncoderBase, RivineBinaryEncoder
from tfchain.encoders.sia import SiaBinaryObjectEncoderBase, SiaBinaryEncoder

BaseRivineObjectEncoder = RivineBinaryObjectEncoderBase
BaseSiaObjectEncoder = SiaBinaryObjectEncoderBase

def encoder_rivine_get():
    return RivineBinaryEncoder()


def encoder_sia_get():
    return SiaBinaryEncoder()


def rivine_encode(*values):
    e = encoder_rivine_get()
    e.add_all(*values)
    return e.data


def sia_encode(*values):
    e = encoder_sia_get()
    e.add_all(*values)
    return e.data
