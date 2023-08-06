from os.path import exists
from typing import Dict
from .path import get_history_path
from .get_batch_sizes import get_batch_sizes
from .dataset import load_dataset

def is_holdout_cached(path:str, batch_size:int, holdout:Dict)->bool:
    return exists("{path}/history.json".format(path=get_history_path(path, batch_size, holdout)))

def is_batch_size_cached(path:str, batch_size:int, settings:Dict)->bool:
    return all([
        is_holdout_cached(path, batch_size, holdout) for holdout in settings["holdouts"]
    ])