from typing import Tuple, Dict
from .model import model
import pandas as pd
from keras.callbacks import EarlyStopping
import auto_tqdm
from environments_utils import is_notebook
from keras_tqdm import TQDMNotebookCallback, TQDMCallback

ktqdm = TQDMNotebookCallback if is_notebook() else TQDMCallback

def fit(training:Tuple, testing:Tuple, batch_size:int, settings:Dict):
    """Train the given model on given train data for the given epochs number.
        training:Tuple,
        testing:Tuple,
        batch_size:int, size for the batch size of this run.
        settings:Dict, the training settings.
    """
    return model(training[0].shape[1]).fit(
        *training,
        verbose=0,
        validation_data=testing,
        **settings["training"]["fit"],
        batch_size=batch_size,
        callbacks=[
            ktqdm(),
            EarlyStopping(**settings["training"]["early_stopping"])
        ]
    )