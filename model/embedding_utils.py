# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 22:57:03 2019

@author: Cheng Lin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 19:40:41 2019

@author: Cheng Lin
"""
import os
import pickle

import numpy as np
# import fasttext

    
def embed_inputs_fasttext(X_train_decoded, ft_model):
    X_train = []
    
    for sample in X_train_decoded:
        X_train_temp = []
        for word in sample:
            word_embedded = ft_model[word]
            X_train_temp.append(word_embedded)
        X_train.append(X_train_temp)
        
    return np.array(X_train)

def embed_inputs_for_lstm(X_train_decoded, tk):
    X_train = []
    
    for sample in X_train_decoded:
        X_train.append(tk.texts_to_matrix(sample, mode='binary'))
    return np.array(X_train)

def embed_inputs_for_embedding_layer(X_train_decoded, tk):
    word_to_int = tk.word_index
    X_train = []
    
    for sample in X_train_decoded:
        X_train_temp = []
        for word in sample:
            index = 0 if word not in word_to_int else word_to_int[word]
            X_train_temp.append(index if index < 6000 else 0)
        X_train.append(np.array(X_train_temp))
    return np.array(X_train)
