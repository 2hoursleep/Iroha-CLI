import click

# ACCOUNT COMMANDS


class CommandsAPI:

    """
    Iroha Commands API utilities
    Supports gRPC & HTTP JSON Transactions & Queries
    """

    def __init__(self, iroha_client):
        self.iroha_client = iroha_client

    # Account Commands

    def create_new_user_account(self):
        user_name = click.prompt("Username For New Account")
        domain = click.prompt("Domain")
        public_key = click.prompt("Public Key")
        self.iroha_client.create_new_account(user_name, domain, public_key)

    def write_account_detail(self):
        account_id = click.prompt("Account To Use : Username@domain")
        key = click.prompt("Enter New Key, existing key entries will be overwritten")
        value = click.prompt("Please enter a value to set")
        self.iroha_client.set_account_detail(account_id, key, value)

    def grant_acc_read_permission(self):
        account_id = click.prompt(
            "Account To Use : Username@domain"
        )
        contact = click.prompt("Username@domain Your Write Acc Granting Permission")
        self.iroha_client.grant_account_read_permission(
            account_id=account_id, contact=contact
        )

        # ASSET COMMANDS#

    def create_new_asset(self):
        asset = click.prompt("New Asset Name Only")
        domain = click.prompt("Domain Name Only")
        precision = click.prompt("Precision", type=int)
        self.iroha_client.create_new_asset(asset, domain, precision)

    def new_asset_transfer(self):
        src_account_id = click.prompt("Source Account", default=account_id)
        recipient = click.prompt("Recipient")
        asset_id = click.prompt("AssetID : asset#domain")
        qty = click.prompt("Total Amount to Send")
        description = click.prompt("Enter Transaction Details")
        self.iroha_client.transfer_asset(
            src_account_id, recipient, asset_id, description, qty
        )

    def increase_asset_qty(self):
        asset_id = click.prompt("AssetID : asset#domain")
        qty = click.prompt("Qty To Add")
        self.iroha_client.add_asset_qty(asset_id, qty)

    def decrease_asset_qty(self):
        asset_id = click.prompt("AssetID : asset#domain")
        qty = click.prompt("Qty To Subtract")
        self.iroha_client.subtract_asset_qty(asset_id, qty)
