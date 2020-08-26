from iroha import primitive_pb2, block_pb2
from iroha import Iroha, IrohaCrypto
import binascii
from time import time

command = Iroha.command

permissions_dict = {
    "can_append_role": primitive_pb2.can_append_role,
    "can_create_role": primitive_pb2.can_create_role,
    "can_detach_role": primitive_pb2.can_detach_role,
    "can_add_asset_qty": primitive_pb2.can_add_asset_qty,
    "can_subtract_asset_qty": primitive_pb2.can_subtract_asset_qty,
    "can_add_peer": primitive_pb2.can_add_peer,
    "can_add_signatory": primitive_pb2.can_add_signatory,
    "can_remove_signatory": primitive_pb2.can_remove_signatory,
    "can_set_quorum": primitive_pb2.can_set_quorum,
    "can_create_account": primitive_pb2.can_create_account,
    "can_set_detail": primitive_pb2.can_set_detail,
    "can_create_asset": primitive_pb2.can_create_asset,
    "can_transfer": primitive_pb2.can_transfer,
    "can_receive": primitive_pb2.can_receive,
    "can_create_domain": primitive_pb2.can_create_domain,
    "can_read_assets": primitive_pb2.can_read_assets,
    "can_get_roles": primitive_pb2.can_get_roles,
    "can_get_my_account": primitive_pb2.can_get_my_account,
    "can_get_all_accounts": primitive_pb2.can_get_all_accounts,
    "can_get_domain_accounts": primitive_pb2.can_get_domain_accounts,
    "can_get_my_signatories": primitive_pb2.can_get_my_signatories,
    "can_get_all_signatories": primitive_pb2.can_get_all_signatories,
    "can_get_domain_signatories": primitive_pb2.can_get_domain_signatories,
    "can_get_my_acc_ast": primitive_pb2.can_get_my_acc_ast,
    "can_get_all_acc_ast": primitive_pb2.can_get_all_acc_ast,
    "can_get_domain_acc_ast": primitive_pb2.can_get_domain_acc_ast,
    "can_get_my_acc_detail": primitive_pb2.can_get_my_acc_detail,
    "can_get_all_acc_detail": primitive_pb2.can_get_all_acc_detail,
    "can_get_domain_acc_detail": primitive_pb2.can_get_domain_acc_detail,
    "can_get_my_acc_txs": primitive_pb2.can_get_my_acc_txs,
    "can_get_all_acc_txs": primitive_pb2.can_get_all_acc_txs,
    "can_get_domain_acc_txs": primitive_pb2.can_get_domain_acc_txs,
    "can_get_my_acc_ast_txs": primitive_pb2.can_get_my_acc_ast_txs,
    "can_get_all_acc_ast_txs": primitive_pb2.can_get_all_acc_ast_txs,
    "can_get_domain_acc_ast_txs": primitive_pb2.can_get_domain_acc_ast_txs,
    "can_get_my_txs": primitive_pb2.can_get_my_txs,
    "can_get_all_txs": primitive_pb2.can_get_all_txs,
    "can_get_blocks": primitive_pb2.can_get_blocks,
    "can_grant_can_set_my_quorum": primitive_pb2.can_grant_can_set_my_quorum,
    "can_grant_can_add_my_signatory": primitive_pb2.can_grant_can_add_my_signatory,
    "can_grant_can_remove_my_signatory": primitive_pb2.can_grant_can_remove_my_signatory,
    "can_grant_can_transfer_my_assets": primitive_pb2.can_grant_can_transfer_my_assets,
    "can_grant_can_set_my_account_detail": primitive_pb2.can_grant_can_set_my_account_detail,
}


def now():
    return int(time() * 1000)


def all_permissions():
    return [
        primitive_pb2.can_append_role,
        primitive_pb2.can_create_role,
        primitive_pb2.can_detach_role,
        primitive_pb2.can_add_asset_qty,
        primitive_pb2.can_subtract_asset_qty,
        primitive_pb2.can_add_peer,
        primitive_pb2.can_add_signatory,
        primitive_pb2.can_remove_signatory,
        primitive_pb2.can_set_quorum,
        primitive_pb2.can_create_account,
        primitive_pb2.can_set_detail,
        primitive_pb2.can_create_asset,
        primitive_pb2.can_transfer,
        primitive_pb2.can_receive,
        primitive_pb2.can_create_domain,
        primitive_pb2.can_read_assets,
        primitive_pb2.can_get_roles,
        primitive_pb2.can_get_my_account,
        primitive_pb2.can_get_all_accounts,
        primitive_pb2.can_get_domain_accounts,
        primitive_pb2.can_get_my_signatories,
        primitive_pb2.can_get_all_signatories,
        primitive_pb2.can_get_domain_signatories,
        primitive_pb2.can_get_my_acc_ast,
        primitive_pb2.can_get_all_acc_ast,
        primitive_pb2.can_get_domain_acc_ast,
        primitive_pb2.can_get_my_acc_detail,
        primitive_pb2.can_get_all_acc_detail,
        primitive_pb2.can_get_domain_acc_detail,
        primitive_pb2.can_get_my_acc_txs,
        primitive_pb2.can_get_all_acc_txs,
        primitive_pb2.can_get_domain_acc_txs,
        primitive_pb2.can_get_my_acc_ast_txs,
        primitive_pb2.can_get_all_acc_ast_txs,
        primitive_pb2.can_get_domain_acc_ast_txs,
        primitive_pb2.can_get_my_txs,
        primitive_pb2.can_get_all_txs,
        primitive_pb2.can_get_blocks,
        primitive_pb2.can_grant_can_set_my_quorum,
        primitive_pb2.can_grant_can_add_my_signatory,
        primitive_pb2.can_grant_can_remove_my_signatory,
        primitive_pb2.can_grant_can_transfer_my_assets,
        primitive_pb2.can_grant_can_set_my_account_detail,
    ]


def genesis_block(users, roles, peers, domains):
    """
    Compose a set of common for all tests' genesis block transactions
    :param admin: dict of id and private key of admin
    :param alice: dict of id and private key of alice
    :param test_permissions: permissions for users in test domain
    :param multidomain: admin and alice accounts will be created in
    different domains and the first domain users will have admin right
    by default if True
    :return: a list of Iroha.command's
    """
    commands = []
    for iroha_peer in peers:
        _add_peer = {
            "addPeer": {
                "peer": {
                    "address": iroha_peer["address"],
                    "peerKey": iroha_peer["peer_key"],
                }
            }
        }
        commands.append(_add_peer)
    for role in roles:
        _add_role = {
            "createRole": {
                "roleName": role["role_name"],
                "permissions": role["permissions"],
            }
        }
        commands.append(_add_role)
    for domain in domains:
        _add_domain = {
            "createRole": {
                "domainId": domain["domain_id"],
                "defaultRole": domain["default_role"],
            }
        }
        commands.append(_add_domain)
    for user in users:
        _add_user = {
            "createAccount": {
                "accountName": user["account_name"],
                "domainId": user["domain_id"],
                "publicKey": user["public_key"],
            }
        }
        commands.append(_add_user)
        for user_role in user["user_roles"]:
            _append_user_role = {
                "appendRole": {
                    "accountId": f'{user["account_name"]}@{user["domain_id"]}',
                    "roleName": user_role,
                }
            }
            commands.append(_append_user_role)
    return commands


def hex(generator):
    """
    Decorator for transactions' and queries generators.
    Allows preserving the type of binaries for Binary Testing Framework.
    """
    prefix = "T" if generator.__name__.lower().endswith("tx") else "Q"
    print(
        "{}{}".format(
            prefix, binascii.hexlify(generator().SerializeToString()).decode("utf-8")
        )
    )
