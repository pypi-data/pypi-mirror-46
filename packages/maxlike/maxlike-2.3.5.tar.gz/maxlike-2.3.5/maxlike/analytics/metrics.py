import numpy as np
from scipy.special import factorial


def log_poisson(y_true, y_pred):
    return (y_true * np.log(y_pred) -
            y_pred - np.log(factorial(y_true))).mean()


def log_loss(y_true, y_pred):
    return ((1 - y_true) * np.log(1 - y_pred) + 
            y_true * np.log(y_pred)).mean()


def accuracy(y_true, y_pred, threshold=.5):
    return (y_true == (y_pred >= threshold)).mean()