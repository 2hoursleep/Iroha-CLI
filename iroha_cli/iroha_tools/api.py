import binascii
from binascii import Error
import json
import pprint
import iroha.primitive_pb2 as iroha_primitive
import iroha.queries_pb2 as queries_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson, ParseDict
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto as ic


class IrohaClientAPI:
    """
    Iroha Client API utilities
    Supports gRPC & HTTP JSON Transactions & Queries
    """

    def __init__(self, ic, creator_account, private_key, iroha_host):
        self.ic = ic
        self.creator_account = creator_account
        self.iroha = Iroha(creator_account)
        self.permissions = iroha_primitive
        self.user_private_key = private_key
        self.net = IrohaGrpc(iroha_host, timeout=60)

    def send_transaction_return_result(self, transaction):
        hex_hash = binascii.hexlify(self.ic.hash(transaction))
        tx_result = {}
        try:
            self.net.send_tx(transaction)
            tx_status = []
            for status in self.net.tx_status_stream(transaction):
                tx_status.append(status)
            tx_result = {
                "tx_hash": hex_hash,
                "tx_statuses": tx_status,
                "tx_result": tx_status[-1][0],
            }
        except Exception as error:
            print(error)
            tx_result = {
                "tx_hash": hex_hash,
                "tx_statuses": [],
                "tx_result": "REJECTED",
            }
        return tx_result

    def send_query_print_status_and_return_result(
        iroha_host_addr, iroha_port, transaction
    ):
        hex_hash = binascii.hexlify(ic.hash(transaction))
        print(f"Transaction hash = {hex_hash}")
        net = IrohaGrpc(f"{iroha_host_addr}:{iroha_port}", timeout=60)
        response = net.send_query(transaction)
        data = MessageToJson(response)
        return data

    def submit_json_tx(self, account_id: str, transaction):
        iroha = Iroha(account_id)
        new_tx = iroha.transaction([])
        iroha_host_addr = "127.0.0.1"
        iroha_port = "50051"
        try:
            transaction = ParseDict(transaction, new_tx)
            print(transaction)
            result = self.send_transaction_return_result(
                iroha_host_addr, iroha_port, transaction
            )
            return result
        except Exception as e:
            print(e)

    def submit_json_query(self, account_id, transaction):
        print("start iroha query")
        # iroha = Iroha(account_id)
        new_tx = queries_pb2.Query()
        print(f"new query {new_tx}")
        try:
            transaction = ParseDict(transaction, new_tx)
            print(transaction)
            return self.send_query_print_status_and_return_result(
                account_id, transaction
            )
        except Exception as e:
            print(e)
