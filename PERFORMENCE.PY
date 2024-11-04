
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
from sklearn.metrics import confusion_matrix
import pandas as pd

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
X_test = df1.iloc[:, 0:2]
X_test = np.reshape(X_test,( 150,2))
y_test  = df1.iloc[:, 2:3]
y_test = np.reshape(y_test, (150, 1))
# print (X_test)
# print (y_test)

acc = model.evaluate(X_test, y_test)
print("Test accuracy = ", acc)

#code tyo genarate confusion_matrix
y_pred = []
pr = model.predict(X_test)
for pi in pr:
    p = np.argmax(pi)
    y_pred.append(p)

y_test = np.reshape(y_test,  150)
print(y_test)
print(y_pred)

cm = confusion_matrix(y_test, y_pred)
print('confusion_matrix')
print(cm)

# confusion_matrix = pandas.DataFrame(cm, index = [i for i in ["chatgpt","human"]],
#                   columns = [i for i in ["chatgpt","human"]])

# plt.figure(figsize = (10,7))
# sn.heatmap(confusion_matrix, annot=True,cmap="YlGnBu", fmt='g')
# plt.show()


