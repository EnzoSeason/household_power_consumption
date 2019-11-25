import numpy as np
import pandas as pd

# charger des données
data_path = '../data/input/household_power_consumption.txt'
df = pd.read_csv(data_path, sep=';', low_memory=False,
                 infer_datetime_format=True, parse_dates={'datetime':[0,1]}, index_col=['datetime'])

# remplir les valeurs manquantes
df.replace('?', np.nan, inplace=True)
df = df.astype('float64')

def remplir_donnees(values):
    one_day = 60 * 24
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            if np.isnan(values[row, col]):
                values[row, col] = values[row - one_day, col]

remplir_donnees(df.values)

# créer la colonne Sub_metering_4
values = df.values
df['sub_metering_4'] = (values[:,0] * 1000 / 60) - (values[:,4] + values[:,5] + values[:,6])

# sauvegarder les données nettoyées
out_dir = '../data/output/'
out_name = 'cleaned_household_power_consumption.csv'
df.to_csv(out_dir + out_name)