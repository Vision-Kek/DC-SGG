import os
import json

def require_exist(alias, realpth):
    if not os.path.exists(realpth):
        print(f"Did you not run the script that generates {alias}?")
        raise FileNotFoundError(f'Dir {alias} does not exist under {realpth}')

def make_exist_ok(alias, realpth):
    if not os.path.exists(realpth):
        print(f"Creating new {alias} dir: {realpth}")
        os.makedirs(realpth)
    else:
        print(f"Using existing {alias} dir: {realpth}")

def open_json(path):
    with open(path) as f:
        return json.load(f)