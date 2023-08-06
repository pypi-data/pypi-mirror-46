import extra_keras_metrics
from extra_keras_utils import set_seed
from keras.models import Sequential
from keras.layers import InputLayer, Dense, Dropout

def model(input_size:int):
    """Return a multi-layer perceptron."""
    set_seed(42)
    model = Sequential([
        InputLayer(input_shape=(input_size,)),
        *[Dense(80, activation="relu") for _ in range(2)],
        Dropout(0.2),
        Dense(1, activation="sigmoid")
    ])
    model.compile(
        optimizer="nadam",
        loss='binary_crossentropy',
        metrics=["auprc", "auroc", "accuracy"]
    )
    return model