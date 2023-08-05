'import BASIC'
import numpy as np
import pandas as pd
import re
import os
import random
'import VISUALIZATION'
import matplotlib.pyplot as plt
'import SKLEARN, SCIPY'
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats.stats import pearsonr
# 'import KERAS'
# import gc
# import tensorflow as tf
# from keras.backend.tensorflow_backend import set_session, get_session, clear_session
# from keras.models import Sequential
# from keras import models
# from keras.applications import VGG19
# from keras import initializers, callbacks, layers, regularizers, optimizers, utils
'import STAT MODELS'
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model

def get_demo():
    print("Formula = x3 + x11 + x5, with h2 = 0.95")
    return pd.read_csv("http://www.zzlab.net/James_Demo/NIH_herb.x"),\
           pd.read_csv("http://www.zzlab.net/James_Demo/NIH_herb.y")

class Model():
    def __init__(self, niter=100, kfold=5, PLS_filter=.2, pid=0):
        self.niter = niter
        self.kfold = kfold
        self.PLS_filter = PLS_filter
        self.pid = pid
        print("Components_Finder(niter=%d, kfold=%d, PLS_filter=%.2f, #ofGPU=%d)"%(self.niter, self.kfold, self.PLS_filter, self.pid))
    def fit(self, xTrain, yTrain):
        yTrain = np.array(yTrain).reshape((len(yTrain)))
        self.agent = Selector(xTrain, yTrain, self.pid)
        self.agent.standardize()
        self.agent.select_by_PLS(top=self.PLS_filter, one_time=True)
    def predict(self, xTest):
        xTest = xTest.loc[:,self.agent.ls_compQC]
        std = StandardScaler()
        std.fit(xTest)
        self.pre, self.wt = self.agent.evaluate_by_models(one_time=True, xTest=std.transform(xTest))
        return np.array(self.pre['rf'])
    def find_compounds(self, x, y, verbose=False):
        'create blank dataframe'
        trait = y.columns[0]
        y = np.array(y[trait])
        dt_wt_out = pd.DataFrame()
        dt_wt_out['comp'] = x.columns
        dt_wt_out[trait] = 0
        for i in range(self.niter):
            if verbose:
                print("Iteration: %d" %(i))
            dt_wt = pd.DataFrame()
            dt_wt['comp'] = x.columns
            agent = Selector(x, y, self.pid)
            agent.train_test_split(kfold=self.kfold)
            agent.select_by_PLS(top=self.PLS_filter)
            # agent.select_by_NN(top=.1)
            dt_wt_sub, r_sub = agent.evaluate_by_models()
            'organize weight'
            dt_wt_merge = pd.merge(dt_wt, dt_wt_sub, how='outer', on='comp')
            val_na = dt_wt_merge.min()[1:]
            dt_wt_merge = dt_wt_merge.fillna(val_na)
            'organize r2-weighted weight'
            mat_wt = np.array(dt_wt_merge.drop(columns='comp'))
            mat_r2 = list(r_sub.values())
            'update weight'
            dt_wt_out[trait] += np.matmul(mat_wt, mat_r2)
            dt_wt_out[trait] = round(dt_wt_out[trait], 5)
        return dt_wt_out.sort_values(by=[trait], ascending=False)

class Selector():
    def __init__(self, dt_x, ls_y, pid):
        self.dt_x = dt_x
        self.ls_y = ls_y
        self.pid = pid
        self.n = len(self.ls_y)
        self.ls_compAll = dt_x.columns
    def standardize(self):
        """For one time prediction"""
        'standardize Y'
        array_Y = np.array(self.ls_y)
        self.ls_y = (array_Y - array_Y.mean())/array_Y.std()
        'standardize X'
        self.scaler = StandardScaler()
        self.scaler.fit(self.dt_x)
        'collect dataset'
        self.data = dict(x = self.scaler.transform(self.dt_x),
                         y = self.ls_y)
    def train_test_split(self, kfold):
        """For validation"""
        'get index'
        ls_idx = np.arange(self.n)
        random.shuffle(ls_idx)
        idx_test = ls_idx[:round(self.n/kfold)]
        idx_train = ls_idx[round(self.n/kfold):]
        'standardize Y'
        array_Y = np.array(self.ls_y)
        self.ls_y = (array_Y - array_Y.mean())/array_Y.std()
        'split dataset'
        self.dt_x_train = self.dt_x.iloc[idx_train]
        self.dt_x_test = self.dt_x.iloc[idx_test]
        self.ls_y_train = self.ls_y[idx_train]
        self.ls_y_test = self.ls_y[idx_test]
        'standardize X'
        scaler = StandardScaler()
        self.dt_x_train = scaler.fit_transform(self.dt_x_train)
        'collect dataset'
        self.data = dict(x_train = scaler.transform(self.dt_x_train),
                         x_test = scaler.transform(self.dt_x_test),
                         y_train = self.ls_y_train,
                         y_test = self.ls_y_test)
    def select_by_PLS(self, top, one_time=False):
        'fitting PLS'
        model_pls = PLSRegression(n_components=10)
        if one_time:
            model_pls.fit(self.data['x'], self.data['y'])
        else:
            model_pls.fit(self.data['x_train'], self.data['y_train'])
        'obtain weights from PLS'
        wt_pls = abs(model_pls.coef_[:,0])
        'get top K features by PLS'
        idx_keyPls = np.where(wt_pls > np.percentile(wt_pls, (1-top)*100))[0]
        self.ls_compQC = self.ls_compAll[idx_keyPls]
        'collect QCed dataset'
        if one_time:
            self.data = dict(x = self.data['x'][:,idx_keyPls],
                             y = self.data['y'])
        else:
            self.data = dict(x_train = self.data['x_train'][:,idx_keyPls],
                             x_test = self.data['x_test'][:,idx_keyPls],
                             y_train = self.data['y_train'],
                             y_test = self.data['y_test'])
    # def select_by_NN(self, top, one_time=False):
    #     self.assignGPU(self.pid)
    #     'Define variables by one_time'
    #     if one_time:
    #         x_train = self.data['x']
    #         y_train = self.data['y']
    #     else:
    #         x_train = self.data['x_train']
    #         y_train = self.data['y_train']
    #     'fitting NN'
    #     act = 'elu'
    #     name_model = "model_%d.h5" % (self.pid)
    #     n = x_train.shape[0]
    #     p = x_train.shape[1]
    #     width = 2**12
    #     model = Sequential()
    #     model.add(layers.Dense(width, activation = act, input_dim = p, name = "AE",activity_regularizer = regularizers.l1_l2(l1 = 1e-3, l2 = 0)))
    #     model.add(layers.Dense(1, activation = "linear"))
    #     model.compile(optimizer= optimizers.Adam(1e-4), loss = 'mse')
    #     # model.summary()
    #     cbList = [callbacks.ModelCheckpoint(monitor = 'loss', mode = 'min',
    #              filepath = name_model, save_best_only = True)]
    #     model.fit(x_train, y_train, verbose = 0,
    #         callbacks = cbList,
    #         epochs = 500)
    #     model.load_weights(name_model)
    #     'grad neurons from the 1st layers'
    #     model_1st = models.Model(inputs = model.input, outputs = model.get_layer("AE").output)
    #     neurons = model_1st.predict(x_train)
    #     'calculate correlation or neuron'
    #     ls_cor = [pearsonr(neurons[:,i], y_train.reshape((n,)))[0] for i in range(width)]
    #     pd.DataFrame(ls_cor).describe()
    #     idx_KeyWeight = abs(np.array(ls_cor)) > np.percentile(np.array(ls_cor), 99)
    #     array_Weight = abs(model.get_weights()[0])
    #     pd_weight = pd.DataFrame(array_Weight).transpose()[idx_KeyWeight]
    #     'obtain weight from NN'
    #     wt_nn = np.sum(pd_weight, axis=0)
    #     'get top K features by NN'
    #     idx_keyNN = np.where(wt_nn > np.percentile(wt_nn, (1-top)*100))[0]
    #     self.ls_compQC = self.ls_compQC[idx_keyNN]
    #     'collect QCed dataset'
    #     if one_time:
    #         self.data = dict(x = self.data['x'][:,idx_keyNN],
    #                          y = self.data['y'])
    #     else:
    #         self.data = dict(x_train = self.data['x_train'][:,idx_keyNN],
    #                          x_test = self.data['x_test'][:,idx_keyNN],
    #                          y_train = self.data['y_train'],
    #                          y_test = self.data['y_test'])
    #     'reset keras'
    #     self.reset_keras(model, self.pid)
    def evaluate_by_models(self, one_time=False, xTest=None):
        'models'
        wt_rf, r2_rf, pre_rf = self.CV_RF(one_time, xTest)#
        wt_glm, r2_glm, pre_glm = self.CV_GLM(one_time, xTest)
        'export weigts'
        dt_wt = pd.DataFrame()
        dt_wt['comp'] = self.ls_compQC
        dt_wt['rf'] = wt_rf#
        dt_wt['glm'] = wt_glm
        if one_time:
            'export prediction'
            dt_pre = pd.DataFrame()
            dt_pre['rf'] = pre_rf
            dt_pre['glm'] = pre_glm
            'return'
            return dt_pre, dt_wt
        else:
            'export acc'
            dic_r2 = dict(rf = r2_rf,
                          glm = r2_glm)#
            # dic_r2 = dict(glm = r2_glm)
            'return'
            return dt_wt, dic_r2
    # def assignGPU(self, gpu):
    #     os.environ["CUDA_VISIBLE_DEVICES"]="%d" % (gpu)
    #     config = tf.ConfigProto()
    #     config.gpu_options.allow_growth = True
    #     set_session(tf.Session(config=config))
    # def reset_keras(self, model, batch):
    #     sess = get_session()
    #     clear_session()
    #     sess.close()
    #     sess = get_session()
    #     'delete model'
    #     try:
    #         del model # this is from global space - change this as you need
    #     except:
    #         pass
    #     for i in range(5):
    #         gc.collect() # if it's done something you should see a number being outputted
    #     'restart session'
    #     self.assignGPU(batch)
    def CV_RF(self, one_time=False, xTest=None):
        'model construction and prediction'
        reg = RandomForestRegressor(n_estimators=30)
        if one_time:
            reg.fit(self.data['x'], self.data['y'])
            'predict'
            yTest = reg.predict(xTest)
            'feature weights'
            wt = np.array(abs(reg.feature_importances_))
            'return'
            return (wt-wt.mean())/wt.std(), None, yTest
        else:
            reg.fit(self.data['x_train'], self.data['y_train'])
            'accuracy'
            r2 = pearsonr(self.data['y_test'], reg.predict(self.data['x_test']))[0]**2
            'feature weights'
            wt = np.array(abs(reg.feature_importances_))
            'return'
            return (wt-wt.mean())/wt.std(), r2, reg.predict(self.data['x_test'])
    def CV_GLM(self, one_time=False, xTest=None):
        'model construction and prediction'
        reg = linear_model.LinearRegression()
        if one_time:
            reg.fit(self.data['x'], self.data['y'])
            'predict'
            yTest = reg.predict(xTest)
            'feature weights'
            wt = np.array(abs(reg.coef_))
            'return'
            return (wt-wt.mean())/wt.std(), None, yTest
        else:
            reg.fit(self.data['x_train'], self.data['y_train'])
            'accuracy'
            r2 = pearsonr(self.data['y_test'], reg.predict(self.data['x_test']))[0]**2
            'feature weights'
            wt = np.array(abs(reg.coef_))
            'return'
            return (wt-wt.mean())/wt.std(), r2, reg.predict(self.data['x_test'])
