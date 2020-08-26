import binascii
from binascii import Error
import json
import pprint
import iroha.primitive_pb2 as iroha_primitive
import iroha.queries_pb2 as queries_pb2
from google.protobuf.json_format import MessageToDict, MessageToJson, ParseDict
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto as ic
from cli import console


class IrohaClient:
    def __init__(self, creator_account, private_key, iroha_host):
        self.creator_account = creator_account
        self.iroha = Iroha(creator_account)
        self.ic = ic
        self.permissions = iroha_primitive
        self.user_private_key = private_key
        self.net = IrohaGrpc(iroha_host, timeout=60)

    def send_batch_and_print_status(self, transactions):

        self.net.send_txs(transactions)
        for tx in transactions:
            hex_hash = binascii.hexlify(ic.hash(tx))
            print("\t" + "-" * 20)
            print(
                "Transaction hash = {}, creator = {}".format(
                    hex_hash, tx.payload.reduced_payload.creator_account_id
                )
            )
            for status in self.net.tx_status_stream(tx):
                print(status)

    def submit_transaction(self, transaction):
        hex_hash = str(binascii.hexlify(self.ic.hash(transaction)), "utf-8")
        tx_result = {}
        msg = f"[bold yellow]Transaction Hash:[/bold yellow] [bold green]{hex_hash}[/bold green] \n[bold yellow]Creator Account ID:[/bold yellow] [bold green]{transaction.payload.reduced_payload.creator_account_id}[/bold green]"
        console.print(msg)
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
            console.print(f"{tx_result}")
        except Exception as error:
            print(error)
            tx_result = {
                "tx_hash": hex_hash,
                "tx_statuses": [],
                "tx_result": "REJECTED",
            }
            console.print(tx_result)
        finally:
            return tx_result

    def send_transaction_print_status_and_return_result(self, transaction):
        """
        Main Transaction submission
        """
        hex_hash = binascii.hexlify(self.ic.hash(transaction))
        msg = f"""
                Transaction Hash:
                \n [bold green]{hex_hash}[/bold green]
                \n
                Creator Account ID:
                \n [bold green]{transaction.payload.reduced_payload.creator_account_id}[/bold green]
                \n"""
        print_msg(msg)
        self.net.send_tx(transaction)
        tx_result = []
        for status in self.net.tx_status_stream(transaction):
            tx_result.append(status)
            print(status)
        tx_result.append(hex_hash)
        return tx_result

    ## Important Function
    def sign_and_submit_tx(self, transaction):
        new_tx = self.iroha.transaction([])
        tx = ParseDict(transaction, new_tx)
        print(tx)
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def check_pending_txs(self):
        query = self.iroha.query("GetPendingTransactions")
        ic.sign_query(query, self.user_private_key)
        response = self.net.send_query(query)
        data = MessageToJson(response)
        return data

    def stream_blocks(self):
        """
        Start incomming stream for new blocks
        """
        # add height
        query = self.iroha.blocks_query()
        ic.sign_query(query, self.user_private_key)
        for block in self.net.send_blocks_stream_query(query):
            pprint("The next block arrived: {}".format(MessageToDict(block)), indent=1)

    def get_signatories(self, account_id):
        """
        List signatories by public key for specified user@domain
        """
        query = self.iroha.query("GetSignatories", account_id=account_id)
        ic.sign_query(query, self.user_private_key)
        response = self.net.send_query(query)
        data = MessageToDict(response)
        return data

    def get_account(self, account_id):
        """
        List Account user@domain
        """
        query = self.iroha.query("GetAccount", account_id=account_id)
        ic.sign_query(query, self.user_private_key)
        response = self.net.send_query(query)
        data = MessageToDict(response)
        return data

    def get_account_details(self, account_id, writer=None, key=None):
        """
        List Account details for user@domain
        """
        query = self.iroha.query(
            "GetAccountDetail", account_id=account_id, writer=writer, key=key
        )
        ic.sign_query(query, self.user_private_key)
        response = self.net.send_query(query)
        data = json.loads(response.account_detail_response.detail)
        return data

    def create_new_account(self, account_name, domain, public_key):
        """
        register new user
        """
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "CreateAccount",
                    account_name=account_name,
                    domain_id=domain,
                    public_key=public_key,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def set_account_detail(self, account_id, key, value):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "SetAccountDetail", account_id=account_id, key=key, value=value
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def create_domain(self, domain_id, default_role):
        """
        register non existing/new domain on network
        """
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "CreateDomain", domain_id=domain_id, default_role="user"
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    ### Dev Batch Functions

    def init_test_balance_batch(self, account_id):
        # Add Dummy Asset Supply For Demo
        qty = "10.00000000"
        description = "Welcome To Ubuntu Exchange"
        currencies = ["BTC", "LTC", "ETH", "XLM", "XMR"]
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "AddAssetQuantity", asset_id="btc#iroha", amount=qty
                ),
                self.iroha.command(
                    "AddAssetQuantity", asset_id="ltc#iroha", amount=qty
                ),
                self.iroha.command(
                    "AddAssetQuantity", asset_id="eth#iroha", amount=qty
                ),
                self.iroha.command(
                    "AddAssetQuantity", asset_id="xlm#iroha", amount=qty
                ),
                self.iroha.command(
                    "AddAssetQuantity", asset_id="xmr#iroha", amount=qty
                ),
                self.iroha.command(
                    "TransferAsset",
                    description=description,
                    src_account_id="admin@iroha",
                    dest_account_id=account_id,
                    asset_id="btc#iroha",
                    amount=qty,
                ),
                self.iroha.command(
                    "TransferAsset",
                    description=description,
                    src_account_id="admin@iroha",
                    dest_account_id=account_id,
                    asset_id="ltc#iroha",
                    amount=qty,
                ),
                self.iroha.command(
                    "TransferAsset",
                    description=description,
                    src_account_id="admin@iroha",
                    dest_account_id=account_id,
                    asset_id="eth#iroha",
                    amount=qty,
                ),
                self.iroha.command(
                    "TransferAsset",
                    description=description,
                    src_account_id="admin@iroha",
                    dest_account_id=account_id,
                    asset_id="xlm#iroha",
                    amount=qty,
                ),
                self.iroha.command(
                    "TransferAsset",
                    description=description,
                    src_account_id="admin@iroha",
                    dest_account_id=account_id,
                    asset_id="xmr#iroha",
                    amount=qty,
                ),
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def grant_account_write_permission(self, account_id):
        """
        grand permission write permission for AccountDetails
        """
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "GrantPermission",
                    account_id=account_id,
                    permission=self.permissions.can_set_my_account_detail,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def grant_account_read_permission(self, account_id):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "GrantPermission",
                    account_id=account_id,
                    permission=self.permissions.can_get_my_acc_detail,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    # add signatory
    # remove signatory
    # find peer and remove peer has been added in v1.1

    def add_peer(self, ip_address, peer_key):
        peer = self.permissions.Peer()
        peer.address = ip_address
        peer.peer_key = peer_key
        tx = self.iroha.transaction([self.iroha.command("AddPeer", peer=peer)])
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def grant_asset_tx_history_permission(self, account_id):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "GrantPermission",
                    account_id=account_id,
                    permission=can_get_my_acc_ast_txs,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def grant_account_tx_history_permission(self, account_id):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "GrantPermission",
                    account_id=account_id,
                    permission=can_get_my_acc_txs,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def create_new_asset(self, asset, domain, precision):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "CreateAsset",
                    asset_name=asset,
                    domain_id=domain,
                    precision=precision,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def transfer_asset(self, account_id, recipient, asset_id, description, qty):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "TransferAsset",
                    src_account_id=account_id,
                    dest_account_id=recipient,
                    asset_id=asset_id,
                    description=description,
                    amount=qty,
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def add_asset_qty(self, asset_id, qty):
        """
        Add asset supply
        """
        tx = self.iroha.transaction(
            [self.iroha.command("AddAssetQuantity", asset_id=asset_id, amount=qty)]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def subtract_asset_qty(self, asset_id, qty):
        """
        Subtract asset supply
        """
        tx = self.iroha.transaction(
            [self.iroha.command("SubtractAssetQuantity", asset_id=asset_id, amount=qty)]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)

    def detach_role_tx(self, account_id, role_name):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "DetachRole", account_id=account_id, role_name=role_name
                )
            ]
        )
        ic.sign_transaction(tx, self.user_private_key)
        self.submit_transaction(tx)
