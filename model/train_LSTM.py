# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 19:40:41 2019

@author: Cheng Lin
"""
import pickle
import sys
from datetime import datetime

import numpy as np
from numpy.random import seed
seed(1)

from tensorflow import set_random_seed
set_random_seed(2)

# import fasttext

from keras.preprocessing.text import Tokenizer
from keras.regularizers import l1
from keras.models import Sequential
from keras.layers import Embedding, Dense, Dropout, Activation
from keras.layers import LSTM

from embedding_utils import embed_inputs_for_embedding_layer


if __name__ == '__main__':
    new_tokenizer = (sys.argv[1] == 'True')
    tokenizer_num = int(sys.argv[2]) 
    epochs = int(sys.argv[3])
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    print('--------------reading in data--------------')
    X_train_decoded = np.load('training_data/X_train.npy')
    y_train = np.load('training_data/y_train.npy')
    
    X_train_decoded = X_train_decoded
    y_train = y_train
    
    print('--------------embedding data--------------')
    if new_tokenizer:
        print('creating a new tokenizer')
        tk = Tokenizer(6000)
        
        bag_of_words = []
        for entry in X_train_decoded:
            bag_of_words.extend(entry)
        
        tk.fit_on_texts([word for word in bag_of_words])
        with open('tokenizer_%s.pkl' % timestamp, 'wb') as f:
            pickle.dump(tk, f)
    else:
        with open('tokenizer_%d.pkl' % tokenizer_num, 'rb') as f:
            tk = pickle.load(f)
    
    # ft_model = fasttext.load_model("model_filename.bin")
    X_train = embed_inputs_for_embedding_layer(X_train_decoded, tk)
    
    print('--------------defining model--------------')
    model = Sequential()
    model.add(Embedding(input_dim=6000, output_dim=60, input_length=105))
    model.add(LSTM(64, input_shape=(105, 60), return_sequences=True,
                   kernel_regularizer=l1(0.001)))
    model.add(LSTM(64, return_sequences=True, kernel_regularizer=l1(0.001)))
    model.add(LSTM(64, kernel_regularizer=l1(0.001)))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='linear', activity_regularizer=l1(0.001)))
    model.add(Activation('sigmoid'))
    
    print('--------------compile model--------------')
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    print('--------------train model--------------')
    X_val_decoded = np.load('training_data/X_val.npy')
    y_val = np.load('training_data/y_val.npy')
    X_val = embed_inputs_for_embedding_layer(X_val_decoded, tk)
    
    model.fit(X_train, y_train, validation_data=(X_val, y_val),
              batch_size=64, epochs=epochs)
    
    print('--------------validate model--------------')
    score = model.evaluate(X_val, y_val, batch_size=32)
    model.save('model_%s.h5' % timestamp)
    print('score: %f' % score[1])
