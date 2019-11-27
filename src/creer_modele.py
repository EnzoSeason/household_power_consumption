import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

def train_valid_diviser(values):
    '''
    diviser un ensemble de données en ensembles train / test par années
    
    Parameters:
    -- values - un np.array avec 2 dimensions
    '''
    # divisées par années
    train, valid = values[1:-328], values[-328:-6]
    return train, valid

def feature_target_split(data, stride = 7):
    '''
    transformer les donnéés dans 2 parties
    
    Parameters:
    -- data - la conso, 1 dimension
    -- slide - nombre de jour choisi pour créer feature. Une samaine (7) par defaut
    '''
    feature = []
    target = []
    
    i_start = 0
    for i in range(len(data)):
        i_end = i_start + stride
        if i_end < len(data):
            feature.append(data[i_start:i_end])
            target.append(data[i_end])
            i_start += 1
    
    return np.array(feature), np.array(target)

def create_step_model(model):
    '''
    ajouter un couche de standardisation et un couche de normalisation avant le modèle de Machine Learning
    '''
    steps = []
    steps.append(('standardize', StandardScaler()))
    steps.append(('normalize', MinMaxScaler()))
    steps.append(('model', model))
    
    step_model = Pipeline(steps=steps)
    return step_model

def recursive_multi_step_forecasting(model, feature):
    '''
    réaliser l'algo Recursive Multi-Step Forecasting
    
    Parameters:
    -- model - le modèle d'un pas du temps
    -- feature - les features qui creéent le modèle d'un pas du temps
    '''
    pred_sequence = []
    history = list(feature)
    stride = len(feature)
    
    for j in range(stride):
        X = np.array(history[-stride:]).reshape(1, stride)
        pred = model.predict(X)[0]
        pred_sequence.append(pred)
        # ajouter la prediction dans les données entrées
        history.append(pred)
    return np.array(pred_sequence)

def model_prediction(model, train, valid, stride=7):
    '''
    prédire les résultat basé sur l'ensemble de train, et elle peut valider par l'ensemble de validation

    Parameters:
    -- model - sklearn model
    -- train, valid - np array avec 2 dimensions
    -- stride - le nombre de jours prédit dans chaque itération
    '''
    history = list(train)
    pred = []
    
    for i in range(0,len(valid),stride):
        train_x, train_y = feature_target_split(history, stride)
        step_model = create_step_model(model)
        step_model.fit(train_x, train_y)
        pred_sequence = recursive_multi_step_forecasting(step_model, train_x[-1, :])
        
        pred.append(pred_sequence)
        # get real observation and add to history for predicting the next day
        history.append(valid[i])
    
    return np.array(pred).flatten()

day_df = pd.read_csv('../data/output/day_cleaned_household_power_consumption.csv', header=0, 
                    infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
train, valid = train_valid_diviser(day_df.values)
train_conso = train[:,0]
valid_conso = valid[:,0]
pred = model_prediction(LinearRegression(), train_conso, valid_conso, stride=7)