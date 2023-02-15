import datetime

with open("debug_state", "r") as f:
    debug_file = f.readline()
DEBUG_STATE = int(debug_file)

def print_debug(output):
    if DEBUG_STATE:
        print(f"{datetime.datetime.now()} | {output}")

def print_log(output):
    print(f"{datetime.datetime.now()} | {output}")
