import json

from functii.debug import DEBUG_STATE

config_dir = "storage/configs/"
config_filename = config_dir + "deb_config.json" if DEBUG_STATE else config_dir + "config.json"

with open(config_filename, "r") as f:
    config = json.load(f)

with open("storage/configs/sql.json", "r", encoding='utf-8') as f:
    SQL_CONFIG = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
DEV_ID = config["DEV_ID"]

def is_dev(ctx):
    return ctx.author.id in DEV_ID
