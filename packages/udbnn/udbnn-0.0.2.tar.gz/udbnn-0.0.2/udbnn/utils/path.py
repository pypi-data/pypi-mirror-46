from typing import List

from typing import Callable
import os

def mkdir(func:Callable):
    def wrapper(*args):
        path = func(*args)
        os.makedirs(path, exist_ok=True)
        return path
    return wrapper

@mkdir
def get_history_path(path:str, batch_size:int, holdout:List):
    return "{path}/run/{batch_size}/{holdout_type}/{holdout}".format(
        path=path,
        batch_size=batch_size,
        holdout_type="chromosomal",
        holdout="+".join([str(c) for c in holdout[0]])
    )