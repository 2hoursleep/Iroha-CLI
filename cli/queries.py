import click


class QueryAPI:

    """
    Iroha Commands API utilities
    Supports gRPC & HTTP JSON Transactions & Queries
    """

    def __init__(self, iroha_client):
        self.iroha_client = iroha_client

    # ACCOUNT QUERIES

    def view_account(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        self.iroha_client.get_account(account_id)

    def view_account_detail(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        writer = click.prompt("Writer To Account", default=None)
        key = click.prompt("Enter A Key", default=None)
        self.iroha_client.get_account_details(account_id)

    def view_signatories(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        self.iroha_client.get_signatories(account_id)

    def query_account_tx_history(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        total = click.prompt("Total Txs to return", default=50)
        self.iroha_client.get_acc_tx_history(account_id=account_id, total=total)

    def query_tx_history(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        total = click.prompt("Total Txs to return", default=50)
        self.iroha_client.get_tx_history(account_id=account_id, total=total)

    def query_pending_txs(self):
        click.echo("Checking For Pending Transactions That Require Signatures")
        self.iroha_client.check_pending_txs()

    def stream_new_blocks(self):
        click.echo("Streaming New Blocks")
        while True:
            self.iroha_client.stream_blocks()

    def view_roles(self):
        click.echo("Getting Roles")
        self.iroha_client.get_roles()

    def view_role_permissions(self):
        role_id = click.prompt("Role ID To View Permissions", default="user")
        self.iroha_client.get_role_permissions(role_id)

    # ASSET QUERIES
    def view_account_asset_balance(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        self.iroha_client.get_account_assets(account_id)

    def grant_asset_read_permission(self):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        contact = click.prompt("Username@domain Your Write Acc Granting Permission")
        self.iroha_client.grant_account_read_permission(
            creator_account=account_id, contact=contact
        )

    def query_asset_tx_history(self, account_id):
        account_id = click.prompt(
            "Account To Use : Username@domain", default=account_id
        )
        total = click.prompt("Total Txs to return", default=50)
        self.iroha_client.get_acc_tx_history(creator_account=account_id, total=total)


# def query_domain_assets():
#   click.echo("Checking For Pending Transactions That Require Signatures")
#   get_domain_assets()
