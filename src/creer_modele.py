import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import pickle

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

    Parametres:
    -- model - le modèle de Sklearn
    '''
    steps = []
    steps.append(('standardize', StandardScaler()))
    steps.append(('normalize', MinMaxScaler()))
    steps.append(('model', model))
    
    step_model = Pipeline(steps=steps)
    return step_model

def recursive_multi_step_forecasting(model, feature):
    '''
    réaliser l'algo Recursive Multi-Step Forecasting,
    la prédiction a la même période que le feature.
    Par exemple, si les données d'entrée sont les données dans une semaine, 
    la fonction va prédire les données de la semaine suivante. 
    
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
    La fonction utilise l'ensemble de train à entraîner le modèle,
    et l'ensemble de validation à prédire

    Parametres:
    -- model - le modèle de Sklearn
    -- train, valid - les données, np.array avec 1 dimension
    -- stride - la période de la prédiction 
    '''
    history = list(train)
    pred = []
    
    # train the model
    train_x, train_y = feature_target_split(history, stride)
    step_model = create_step_model(model)
    step_model.fit(train_x, train_y)
    input_data = train_x[-1, :]
    
    for i in range(0,len(valid),stride):
        pred_sequence = recursive_multi_step_forecasting(step_model, input_data)
        pred.append(pred_sequence)
        # charger les données d'une semaine prochaine pour faire la prédiction suivante
        input_data = valid[i:i+stride]
    
    return step_model, np.array(pred).flatten()

# ==============================================

day_df = pd.read_csv('../data/output/day_cleaned_household_power_consumption.csv', header=0, 
                    infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
train, valid = train_valid_diviser(day_df.values)
train_conso = train[:,0]
valid_conso = valid[:,0]
step_model, pred = model_prediction(LinearRegression(), train_conso, valid_conso, stride=7)
# sauvegarder les résultats
with open('../data/output/step_model.pkl', 'wb') as f:
    pickle.dump(step_model, f)
np.savetxt('../data/output/training_set.csv', train_conso, delimiter=",")
np.savetxt('../data/output/validation_set.csv', valid_conso, delimiter=",")
np.savetxt('../data/output/prediction.csv', pred, delimiter=",")