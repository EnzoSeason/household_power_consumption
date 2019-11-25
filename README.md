# Consommation électrique individuelle des ménages

[La Consommation électrique des ménages](https://archive.ics.uci.edu/ml/datasets/Individual+household+electric+power+consumption) est un jeu de données temporelles multivariées décrivant la consommation d'électricité d'un seul ménage sur quatre ans.

Les données ont été collectées entre décembre 2006 et novembre 2010 et des observations de la consommation d'énergie au sein du ménage ont été collectées chaque minute.

C'est une série multivariée composée de sept variables (en plus de la date et de l'heure).

1. date: Date in format dd/mm/yyyy 
2. time: time in format hh:mm:ss 
3. global_active_power: household global minute-averaged active power (in kilowatt) 
4. global_reactive_power: household global minute-averaged reactive power (in kilowatt) 
5. voltage: minute-averaged voltage (in volt) 
6. global_intensity: household global minute-averaged current intensity (in ampere) 
7. sub_metering_1: energy sub-metering No. 1 (in watt-hour of active energy). It corresponds to the kitchen, containing mainly a dishwasher, an oven and a microwave (hot plates are not electric but gas powered). 
8. sub_metering_2: energy sub-metering No. 2 (in watt-hour of active energy). It corresponds to the laundry room, containing a washing-machine, a tumble-drier, a refrigerator and a light. 
9. sub_metering_3: energy sub-metering No. 3 (in watt-hour of active energy). It corresponds to an electric water-heater and an air-conditioner.

## Nettoyer les données

D'abord, je **fusionne les prémière et deuxième colonnes dans une colonne**. La nouvelle colonne doit être dans le format `datetime`. Elle est aussi l'indice de données. C'est pour facilité de traitement.

Ensuite, je **remplis les valeurs manquantes**. Dans les informations des données, il a indiqué qu'il y a les values manquantes.

<img src="./data/output/images/missing_value.png">

Donc, je replace `?` par `NaN`. Après, je transforme tous les valeurs numériques dans le format `float`, et remplis ces valeurs manquantes par les mêmes données de la même heure la veille.

A la fin, je **créer la colonne `Sub_metering_4`**. Dans les informations, il a aussi indiqué que l'énergie active consommée chaque minute (en wattheures) dans le ménage par du matériel électrique non mesuré dans les `Sub_metering_1, 2 et 3` est calculé par `(global_active_power*1000/60 - sub_metering_1 - sub_metering_2 - sub_metering_3)`. Donc, je le mets dans la colonne `Sub_metering_4`.

Les données nettoyées sont présenté ici.
<img src="./data/output/images/cleaned_data.png">