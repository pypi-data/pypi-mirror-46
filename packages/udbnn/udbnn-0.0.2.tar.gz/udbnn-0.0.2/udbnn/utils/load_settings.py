import json

def load_settings(path:str):
    with open("{path}/settings.json".format(path=path), "r") as f:
        return json.load(f)