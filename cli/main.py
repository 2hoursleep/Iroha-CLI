from os import close
import click
from .commands import CommandsAPI
from .queries import QueryAPI
from .iroha_tools.client import IrohaClient

# from .asset_commands import new_asset, increase_asset_qty,decrease_asset_qty,new_asset_transfer
from .menu_nav import menu_text, main_options, commands_menu, welcome_msg
from . import console, print_msg

global account_id
global private_key


def iroha_health_check(iroha_client, account_id):
    status = False
    try:
        result = iroha_client.get_account(account_id)
        console.print(f"iroha health check {result}")
        status = True
    except Exception as error:
        console.print(
            f"[bold red]iroha health chech failed[/bold red] \n [bold yellow]{error}[/bold yellow] \n"
        )
        status = False
    finally:
        return status


def main_menu_options():
    print_msg(menu_text)
    user_choice = click.prompt("Please Select Your Option", show_choices=menu_text)
    if user_choice == "1":
        user_choice = None
        print_msg(commands_menu)
        commands_main_menu()
    if user_choice == "4":
        pass
        # iroha_health_check(iroha_client=iroha,account_id=None)
    if user_choice == "exit":
        pass
    else:
        click.echo("Please Select Correct Option")
        user_choice = None


def commands_main_menu():
    global iroha_client
    global account_id
    iroha_commands = CommandsAPI(iroha_client)
    user_choice = click.prompt("Please Select Your Option", show_choices=main_options)
    if user_choice == "1":
        iroha_commands.create_new_user_account()
        commands_main_menu()
    elif user_choice == "2":
        iroha_commands.write_account_detail(account_id)
    if user_choice == "b":
        main_menu_options()


def main_menu(account_id, private_key, iroha_host):
    global iroha_client
    iroha_client = IrohaClient(account_id, private_key, iroha_host)
    user_choice = None
    console.print(welcome_msg)
    console.print(f"Logged in as: {account_id}")
    console.print(f"Private Key: \n {str(private_key, 'utf-8')}")
    while user_choice != "exit":
        main_menu_options()
    print_msg(
        "exiting....\n Thank You  <[-_-]>... \n Developed By Farren Jackson (Distributed Ledger Solutions ZA)"
    )
