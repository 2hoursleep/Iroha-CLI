import binascii
from binascii import Error
import json
import pprint
import iroha.primitive_pb2 as iroha_primitive
import iroha.queries_pb2 as queries_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson, ParseDict
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto


class IrohaUtils:
    """
    Iroha helper utilities
    """

    def __init__(self):
        self.ic = IrohaCrypto

    def save_keys_to_file(self, account_id):
        private_key = self.ic.private_key()
        public_key = self.ic.derive_public_key(private_key)
        try:
            with open(f"{account_id}.priv", "wb+") as private_key_file:
                private_key_file.write(private_key)
            with open(f"{account_id}.priv", "wb+") as public_key_file:
                public_key_file.write(public_key)
            return True
        except Error as error:
            return error

    def generate_keypair(self):
        private_key = self.ic.private_key()
        public_key = str(ic.derive_public_key(private_key), "utf-8")
        private_key = str(private_key, "utf-8")
        key_pair = {"public_key": f"{public_key}", "private_key": f"{private_key}"}
        return json.dumps(key_pair, indent=4)
