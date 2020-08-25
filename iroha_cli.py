#!/usr/bin/python3

import click
from rich.console import Console
from PyInquirer import prompt, print_json
from cli.main import main_menu
from cli.iroha_tools.utils import IrohaUtils
from cli.iroha_tools.commons import permissions_dict

console = Console(width=30)
style = "bold white on red"

@click.group()
def cli():
    pass


@cli.command(name="cli")
@click.option(
    "-a",
    "--account_id",
    type=str,
    envvar="ACCOUNT_ID",
    help="your Iroha Account ID including Domain Name \n e.g: 2hoursleep@iroha",
)
@click.option(
    "-ip",
    "--iroha_host",
    type=str,
    default="localhost:50051",
    envvar="IROHA_HOST",
    help="Iroha Node Address IP:PORT or DNS \n e.g: 2hoursleep@iroha",
)
@click.option(
    "-pk", "--private_key", type=str, help="your Account ID for Keypair file",
)
def main(account_id, iroha_host,private_key):
    if not account_id:
        questions = [
            {
                "type": "input",
                "name": "account_id",
                "message": "What's your account id? username@domain",
            }
        ]
        answers = prompt(questions)
        account_id = answers["account_id"]
    if not private_key:
        private_key_file = f"./{account_id}.priv"
        private_key = open(private_key_file, "rb+").read()
    main_menu(account_id=account_id, iroha_host=iroha_host, private_key=private_key)


@cli.command(name="gen-keys")
@click.option(
    "-a", "--account_id", type=str, help="your Account ID for Keypair file",
)
def generate_user_keypair(account_id):
    iroha_utils = IrohaUtils()
    if not account_id:
        questions = [
            {
                "type": "input",
                "name": "account_id",
                "message": "What's your account id? username@domain",
            }
        ]
        answers = prompt(questions)
        account_id = answers["account_id"]
    console.print(
        f"Generating new keypair for \n {account_id}", style=style, justify="center"
    )
    iroha_utils.save_keys_to_file(account_id)
    console.print(
        f"done\n {account_id}", style=style, justify="center"
    )

@cli.command(name="genesis-block")
@click.option(
    "-a", "--account_id", type=str, help="your Admin Account ID for Keypair file",
)
@click.option(
    "-pk", "--private_key", type=str, help="Private Key In ED2556 String Format",
)
def generate_user_keypair(account_id,private_key):
    iroha_utils = IrohaUtils()
    if not account_id:
        questions = [
            {
                "type": "input",
                "name": "account_id",
                "message": "What's your account id with admin keypair? admin@domain",
            }
        ]
        answers = prompt(questions)
        account_id = answers["account_id"]
    
    iroha_utils.genesis_tx(users, roles, peers, domains, admin_private_key)
    console.print(
        f"done\n {account_id}", style=style, justify="center"
    )

if __name__ == "__main__":
    cli()
