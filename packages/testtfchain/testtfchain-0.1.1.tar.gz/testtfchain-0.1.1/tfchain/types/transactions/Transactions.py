from tfchain.types.transactions.Base import TransactionBaseClass, TransactionVersion
from tfchain.types.transactions.Standard import TransactionV1
from tfchain.types.transactions.Minting import TransactionV128, TransactionV129
from tfchain.types.transactions.ThreeBot import TransactionV144, TransactionV145, TransactionV146
from tfchain.types.transactions.ERC20 import TransactionV208, TransactionV209, TransactionV210

from tfchain.internal.jsutils import json_loads
from tfchain.errors import UnknownTransansactionVersion 

def new():
    """
    Creates and returns a default transaction.
    """
    return TransactionV1()

def mint_definition_new():
    """
    Creates and returns an empty Mint Definition transaction.
    """
    return TransactionV128()

def mint_coin_creation_new():
    """
    Creates and returns an empty Mint CoinCreation transaction.
    """
    return TransactionV129()

def threebot_registration_new():
    """
    Creates and returns an empty 3Bot Registration transaction.
    """
    return TransactionV144()

def threebot_record_update_new():
    """
    Creates and returns an empty 3Bot Record Update transaction.
    """
    return TransactionV145()

def threebot_name_transfer_new():
    """
    Creates and returns an empty 3Bot Name Transfer transaction.
    """
    return TransactionV146()

def erc20_convert_new():
    """
    Creates and returns an empty ERC20 Convert transaction.
    """
    return TransactionV208()

def erc20_coin_creation_new():
    """
    Creates and returns an empty ERC20 Coin Creation transaction.
    """
    return TransactionV209()

def erc20_address_registration_new():
    """
    Creates and returns an empty ERC20 Address Registration transaction.
    """
    return TransactionV210()

def from_json(obj, id=None):
    """
    Create a TFChain transaction from a JSON string or dictionary.

    @param obj: JSON-encoded str, bytes, bytearray or JSON-decoded dict that contains a raw JSON Tx.
    """
    if isinstance(obj, (str, bytes, bytearray)):
        obj = json_loads(obj)
    if not isinstance(obj, dict):
        raise TypeError(
            "only a dictionary or JSON-encoded dictionary is supported as input: type {} is not supported", type(obj))
    tt = obj.get('version', -1)

    txn = None
    if tt == TransactionVersion.STANDARD:
        txn = TransactionV1.from_json(obj)
    elif tt == TransactionVersion.THREEBOT_REGISTRATION:
        txn = TransactionV144.from_json(obj)
    elif tt == TransactionVersion.THREEBOT_RECORD_UPDATE:
        txn = TransactionV145.from_json(obj)
    elif tt == TransactionVersion.THREEBOT_NAME_TRANSFER:
        txn = TransactionV146.from_json(obj)
    elif tt == TransactionVersion.ERC20_CONVERT:
        txn = TransactionV208.from_json(obj)
    elif tt == TransactionVersion.ERC20_COIN_CREATION:
        txn = TransactionV209.from_json(obj)
    elif tt == TransactionVersion.ERC20_ADDRESS_REGISTRATION:
        txn = TransactionV210.from_json(obj)
    elif tt == TransactionVersion.MINTER_DEFINITION:
        txn = TransactionV128.from_json(obj)
    elif tt == TransactionVersion.MINTER_COIN_CREATION:
        txn = TransactionV129.from_json(obj)
    elif tt == TransactionVersion.LEGACY:
        txn = TransactionV1.legacy_from_json(obj)

    if isinstance(txn, TransactionBaseClass):
        txn.id = id
        return txn

    raise UnknownTransansactionVersion("transaction version {} is unknown".format(tt))
