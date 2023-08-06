import gc
import time
import json
import warnings
import itertools
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt

from tqdm                    import tqdm
from time                    import gmtime, strftime
from itertools               import islice
from sklearn.metrics         import *
from sklearn.model_selection import *
from sklearn.preprocessing   import *
from sklearn.externals       import joblib

from scipy.stats          import rankdata
from scipy.special        import erfinv

import keras.backend as K
from keras.optimizers     import adam, sgd
from keras.models         import Model, Sequential
from keras.callbacks      import ModelCheckpoint, EarlyStopping, LearningRateScheduler
from keras.layers         import Dense, Dropout, Input, Embedding, Flatten, Merge, Reshape, BatchNormalization

from IPython.display      import display
from pandas_summary       import DataFrameSummary
from sklearn.svm          import SVC, SVR
from sklearn.tree         import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors    import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble     import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, ElasticNet, Lasso, Ridge
from sklearn.ensemble     import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.ensemble     import AdaBoostClassifier, AdaBoostRegressor, ExtraTreesClassifier, ExtraTreesRegressor

def loadConfig(path):
    parser  = argparse.ArgumentParser()
    parser.add_argument('--config', default=path)
    options = parser.parse_args()
    config  = json.load(open(options.config))
    return config

def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

class tick_tock:
    def __init__(self, process_name, verbose=1):
        self.process_name = process_name
        self.verbose = verbose
    def __enter__(self):
        if self.verbose:
            print(self.process_name + " begin ......")
            self.begin_time = time.time()
    def __exit__(self, type, value, traceback):
        if self.verbose:
            end_time = time.time()
            print(self.process_name + " end ......")
            print('time lapsing {0} s \n'.format(end_time - self.begin_time))

class callbacks_keras:
    def __init__(self, filepath, model,
                 base_lr=1e-3, decay_rate=1,
                 decay_after_n_epoch=10, patience=20,
                 mode='min', monitor='val_loss'):
        self.base_lr = base_lr
        self.model = model
        self.decay_rate = decay_rate
        self.decay_after_n_epoch = decay_after_n_epoch
        self.callbacks = [ModelCheckpoint(filepath = filepath,
                                          monitor = monitor,
                                          verbose = 2,
                                          save_best_only = True,
                                          save_weights_only = True,
                                          mode = mode),
                         EarlyStopping(monitor = monitor, patience = patience, verbose=2, mode = mode),
                         LearningRateScheduler(self._scheduler)]

    def _scheduler(self, epoch):
        if epoch%self.decay_after_n_epoch==0 and epoch!=0:
            lr = K.get_value(self.model.optimizer.lr)
            K.set_value(self.model.optimizer.lr, lr*self.decay_rate)
            print("lr changed to {}".format(lr*self.decay_rate))
        return K.get_value(self.model.optimizer.lr)

def ka_xgb_r2_error(preds, dtrain):
    labels = dtrain.get_label()
    return 'error', r2_score(labels, preds)

def ka_xgb_r2_exp_error(preds, dtrain):
    labels = dtrain.get_label()
    preds = np.clip(np.exp(preds),0, 1e10)
    return 'error', r2_score(np.exp(labels), preds)

def ka_erfinv_rank_transform(x):
    '''
        This is used on numeric variable, after doing this operation, one should do MM and SS on all dataset.
    '''
    mm = MinMaxScaler()
    tmp = erfinv(np.clip(np.squeeze(mm.fit_transform(rankdata(x).reshape(-1,1))), 0, 0.999999999))
    tmp = tmp - np.mean(tmp)
    return tmp

def kaggle_points(n_teams, n_teammates, rank, t=1):
    return (100000 / np.sqrt(n_teammates)) * (rank ** (-0.75)) * (np.log10(1 + np.log10(n_teams))) * (np.e**(t/500))
######################################################################################################
# read and write file functions
######################################################################################################
def mkdir(path):
    '''
        If directory exsit, do not make any change
        Else make a new directory
    '''
    try:
        os.stat(path)
    except:
        os.mkdir(path)

def ka_dict_head(dic, n):
    '''
        first n rows of a dictionary
    '''
    return list(islice(dic, n))

def ka_sort_dict(a, by_key=False, reverse=False):
    '''
        sort dictionary by item or key.
    '''
    sorted_x = sorted(a.items(), key=operator.itemgetter(1-by_key), reverse=reverse)
    return sorted_x
