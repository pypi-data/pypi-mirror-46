import pandas as pd
import numpy as np
import random

def get_split(dt_x, dt_y, ratio_test=.2):
    '''
    input pandas dataframe for x and y
    return dt_x_train, dt_y_train, dt_x_test, dt_y_test
    '''
    idx_random = np.arange(len(dt_x))
    random.shuffle(idx_random)
    '''Split data'''
    n_test = round(len(dt_x)*.2)
    dt_x_train = dt_x.iloc[idx_random[n_test:]]
    dt_y_train = dt_y.iloc[idx_random[n_test:]]
    dt_x_test = dt_x.iloc[idx_random[:n_test]]
    dt_y_test = dt_y.iloc[idx_random[:n_test]]
    '''Return'''
    return dt_x_train, dt_y_train, dt_x_test, dt_y_test
