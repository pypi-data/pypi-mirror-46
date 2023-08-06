from .utils import load_settings
import os
from glob import glob
import shutil

def clear(target:str):
    for dataset in load_settings(target)["datasets"]:
        path = "{target}/{path}/run".format(target=target, path=dataset["path"])
        if os.path.exists(path):
            shutil.rmtree(path)
        for csv in glob("{target}/{path}/*.csv".format(target=target, path=dataset["path"])):
            os.remove(csv)