import pandas as pd
from cli.iroha_tools.utils import IrohaUtils
import json
# from rich import Console
from pprint import PrettyPrinter
import os

iroha_tools = IrohaUtils()

df = pd.read_json("genesis_block.json")
peers = df["genesis_block"]["peers"]
roles = df["genesis_block"]["roles"]
users = df["genesis_block"]["users"]
domains = df["genesis_block"]["domains"]

admin_private_key = os.getenv(
    "IROHA_ADMIN_KEY",
    "673d7a44dd32db621a2148bd89141cc1857cc7c704a998b9bc490238ddf44f25",
)  # admin@test secret from Iroha Github
tx = iroha_tools.genesis_tx(
    users=users,
    roles=roles,
    peers=peers,
    domains=domains,
    admin_private_key=admin_private_key,
)

with open("./genesis.block.template", "r+") as genesis_json:
    genesis_dict = json.load(genesis_json)
    genesis_dict["block_v1"]["payload"]["transactions"][0]["payload"]["reducedPayload"][
        "commands"
    ] = tx
    with open("./new_genesis.block", "w+") as new_genesis_block:
        json.dump(genesis_dict, new_genesis_block, sort_keys=True, indent=3)
        print("done")
