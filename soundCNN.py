import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy.io import wavfile
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, TimeDistributed
from keras.layers import Conv2D, LSTM, MaxPooling2D, CuDNNLSTM, Bidirectional
from keras.optimizers import SGD, Adam

import wave

class WifiCNN:
    def __init__(self):
        self.totalXData = []
        self.totalYData = np.array([[1000],[2000],[3000]])
        self.X_gridData = []
        self.filenames = ['16401__pitx__muted-guitar-c.wav','95328__ramas26__c.wav']

    def open_wave_data(self):
        fs, data = wavfile.read('95328__ramas26__c.wav')
        X_data = data[3000:93000]
        X_data = np.copy(X_data)
        X_data = self.amplitudeMod(X_data, change=4, start=0, end=30000)
        self.totalXData = X_data
        plt.plot(X_data)
        plt.show()

        X_ampl = np.copy(X_data)
        X_rand = np.copy(X_data)
        X_ampl = self.amplitudeMod(X_ampl, change =4,start = 0,end = 30000)
        self.totalXData=np.append(self.totalXData, X_ampl)
        plt.plot(X_ampl)
        plt.show()

        X_rand = self.randomChanges(X_rand,10,2,20000)
        self.totalXData=np.append(self.totalXData, X_rand)
        plt.plot(X_rand)
        plt.show()

        maxs = max(self.totalXData)/2
        self.totalXData = np.divide(self.totalXData,maxs)
        self.totalYData = np.divide(self.totalYData, maxs)

        self.X_gridData = np.array(np.reshape(self.totalXData,(3,300,300,1)))
        plt.plot(self.totalXData)
        plt.show()
        #print(self.X_gridData)
        #plt.plot(self.X_gridData[0][1])
        #plt.show()





    def amplitudeMod(self, data, change, start, end):
        data[start:end+1] = np.divide(data[start:end+1],change)
        return data

    def randomChanges(self, data, num_changes, start=0,end=10000000):
        if(end==10000000):
            leng = len(data)
        else:
            leng = end
        for x in range(num_changes):
            loc = np.random.random_integers(start,leng)
            szes = data.max()
            randnum = np.random.random_integers(-szes, szes)
            data[loc]= randnum
        return data


    def cnn(self):
        #X_train, X_test, y_train, y_test = train_test_split(self.totalXData, self.totalYData, test_size=0.3, random_state=234)
        model = Sequential()
        model.add(Conv2D(30, (2, 2), input_shape=(300, 300, 1), activation='relu'))
        model.add(Conv2D(30,(3,3)))
        model.add(Conv2D(20, (3, 3)))
        model.add(Conv2D(10, (3, 3)))
        model.add(MaxPooling2D(pool_size=(1,1)))
        model.add(Flatten())
        model.add(Dense(10,activation='relu'))
        model.add(Dense(1,activation='softmax'))
        model.compile(loss = 'mean_squared_error', optimizer='rmsprop',metrics=['accuracy'])
        model.summary()
        model.fit(self.X_gridData, self.totalYData,epochs=4,validation_split=0.3)
        score = model.evaluate(self.X_gridData, self.totalYData, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def cnn_data(self):
        print("helo")



if __name__ == '__main__':
    wcnn = WifiCNN()
    wcnn.open_wave_data()
    wcnn.cnn()
    #wcnn.get_value_average()
    #for x in range(1):

