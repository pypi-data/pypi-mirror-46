import pandas as pd
from typing import Tuple, Dict, Callable
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from .ungzip import ungzip
from os.path import exists
import numpy as np
from holdouts_generator import holdouts_generator, chromosomal_holdouts

def load_dataset(path:str, max_correlation:float)->Tuple[pd.DataFrame, pd.DataFrame]:
    if not exists("{path}/x.csv".format(path=path)):
        ungzip("{path}/x.csv.gz".format(path=path))
    if not exists("{path}/y.csv".format(path=path)):
        ungzip("{path}/y.csv.gz".format(path=path))
    x = pd.read_csv("{path}/x.csv".format(path=path), index_col=0).astype(float)
    x = x.drop(columns=x.columns[np.any(np.triu(x.corr()>max_correlation, k=1), axis=1)])
    return (x, pd.read_csv("{path}/y.csv".format(path=path), index_col=0))

def scale(train:pd.DataFrame, test:pd.DataFrame)->Tuple[pd.DataFrame, pd.DataFrame]:
    """Return scaler, scaled training and test vectors based on given training vector."""
    scaler = MinMaxScaler().fit(train)
    return scaler.transform(train), scaler.transform(test)

def normalized_holdouts_generator(dataset:Tuple[pd.DataFrame, pd.DataFrame], holdouts:Dict)->Callable:
    """Return the given dataset split among training a test set for the given random holdout.
        dataset:Tuple[np.ndarray, np.ndarray], the dataset to split.
        holdouts:Dict, the settings relative to the holdouts
    """
    generator = holdouts_generator(*dataset, holdouts=chromosomal_holdouts(holdouts))
    def scaler():
        for (training, testing), _ in generator():
            x_train, x_test = scale(training[0], testing[0])
            yield (x_train, training[1]), (x_test, testing[1])
    return scaler