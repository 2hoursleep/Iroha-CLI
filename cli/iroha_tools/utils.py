import binascii
from binascii import Error
import json
import pprint
from iroha import block_pb2
import iroha.primitive_pb2 as iroha_primitive
import iroha.queries_pb2 as queries_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson, ParseDict
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
from .commons import genesis_block


class IrohaUtils:
    """
    Iroha helper utilities
    """

    def __init__(self):
        self.ic = IrohaCrypto
        self.iroha = Iroha("admin@test")

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
        public_key = str(self.ic.derive_public_key(private_key), "utf-8")
        private_key = str(private_key, "utf-8")
        key_pair = {"public_key": f"{public_key}", "private_key": f"{private_key}"}
        return json.dumps(key_pair, indent=4)

    def genesis_tx(self, users, roles, peers, domains, admin_private_key):
        genesis_block_unsigned = genesis_block(users, roles, peers, domains)
        private_key = bytes(admin_private_key, "utf-8")
        print(private_key)
        # init_tx = self.iroha.transaction(genesis_block_unsigned)
        # tx = self.ic.sign_transaction(init_tx,private_key)
        result = {}
        # dict_tx = MessageToDict(genesis_block_unsigned)
        # block = block_pb2.Block_v1.Payload = dict_tx
        return genesis_block_unsigned
