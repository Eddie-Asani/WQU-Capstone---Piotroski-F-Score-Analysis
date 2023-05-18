## EA test model

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model

data = pd.read_csv('company.csv', index_col=0)
tickers = data.index.tolist()
X = data.values


##In order to decrease the dataset's complexity to a lesser amount of elements, we are going to implement PCA to it.:


n_components = 20 # Dimensionality reduction values

pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X)


## Data Splits into testing & training:

X_train, X_test, y_train, y_test = train_test_split(X_pca, returns, test_size=0.2, random_state=42)


## Data set definition and PCA tranformation with regards to NN :


input_layer = Input(shape=(n_components,))
x = Dense(128, activation='relu')(input_layer)
x = Dense(64, activation='relu')(x)
x = Dense(32, activation='relu')(x)
output_layer = Dense(1, activation='linear')(x)

model = Model(inputs=input_layer, outputs=output_layer)
model.compile(optimizer='adam',
              loss='mse',
              metrics=['mse', 'mae'])

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))


## Lastly, we can utilize the trained model to forecast outcomes using current, unaltered data:


tickers_new = [] # example list of new tickers to predict returns for
data_new = pd.read_csv('final.csv', index_col=0).loc[tickers_new, :].values
X_new = pca.transform(data_new)
y_pred = model.predict(X_new)
