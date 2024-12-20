
from operator import gt, le
import random
import gym 
import keras
import numpy as np
import pandas
from sklearn.model_selection import train_test_split
import tensorflow as tf
from collections import deque
from keras.src import Sequential 
from keras.src.layers import Dense
from keras.src.optimizers import Adam
from devices import STATE
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
import pandas as pd

DATASETSIZE =150
state_size = 2
learning_rate = 0.001
action_size = 4

def build_model():
    model = Sequential() 
    model.add(Dense(32, activation="relu",
                    input_dim= state_size))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(action_size, activation="linear"))
    model.compile(loss="mse",
                    optimizer=Adam(learning_rate=learning_rate))
    model.load_weights('weights_1500.weights.h5')
    return model

model = build_model()
model.summary()

df1 = pd.read_csv('RL_dataSet.csv')
#print(df1)
X_test = df1.iloc[:, 0:2]
#print(X_test)
X_test = np.reshape(X_test,( DATASETSIZE,2))
#print(X_test)
y_test  = df1.iloc[:, 2:3]
#print(y_test)
y_test = np.reshape(y_test, (DATASETSIZE, 1))
#print(y_test)

acc = model.evaluate(X_test, y_test,verbose=0)
print("Accuracy = ", acc)

#code tyo genarate confusion_matrix
y_pred = []
pr = model.predict(X_test)
for pi in pr:
    p = np.argmax(pi)
    y_pred.append(p)

y_test = np.reshape(y_test,  DATASETSIZE)
#print(y_test)
#print(y_pred)

cm = confusion_matrix(y_test, y_pred)
print('confusion_matrix')
print(cm)

confusion_matrix = pandas.DataFrame(cm, index = [i for i in ["UP","DOWN","BALANCE"]],
                  columns = [i for i in ["UP","DOWN","BALANCE"]])

plt.figure(figsize = (10,7))
sn.heatmap(confusion_matrix, annot=True,cmap="YlGnBu", fmt='g')
plt.show()

# calculate precision python
precision = precision_score(y_test, y_pred, average='micro')
print('Precision: %.3f' % precision)

# calculate recall in python
recall = recall_score(y_test, y_pred, average='micro')
print('Recall: %.3f' % recall)

# calculate score
score = f1_score(y_test, y_pred, average='micro')
print('F-Measure: %.3f' % score)
