import pandas as pd
from iroha_cli.iroha_tools.commons import genesis_block
import json
# from rich import Console
import os

def generate_genesis_block(file_path, new_block_name):
    """
    Accepts JSON-style template genesis block file
    parses values and creates Iroha v1 compatible genesis block
    :param file_path: list of users containing name,
    :param new_block_name: str new file name for genesis block
    saves block to cwd
    
    :returns
    """
    tx = []
    try:
        genesis_json_input = pd.read_json(file_path)
        peers = genesis_json_input["genesis_block"]["peers"]
        roles = genesis_json_input["genesis_block"]["roles"]
        users = genesis_json_input["genesis_block"]["users"]
        domains = genesis_json_input["genesis_block"]["domains"]
        tx = genesis_block(
            users=users,
            roles=roles,
            peers=peers,
            domains=domains
        )
    except Exce as error:
    with open("./genesis.block.template", "r+") as genesis_json:
        genesis_dict = json.load(genesis_json)
        genesis_dict["block_v1"]["payload"]["transactions"][0]["payload"]["reducedPayload"][
            "commands"
        ] = tx
        with open("./new_genesis.block", "w+") as new_genesis_block:
            json.dump(genesis_dict, new_genesis_block, sort_keys=True, indent=3)
            print("done")