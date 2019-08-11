# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 19:40:41 2019

@author: Cheng Lin
"""
import os
import pdb
import re
from collections import deque

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def get_array_from_deque(queue):
    temp = []
    for entry in queue:
        temp.extend(entry)
    return temp


if __name__ == '__main__':
    data = []
    labels = []
    
    for filename in os.listdir('../scraping/data/lyrics/'):
        # read in csv of data
        print(filename)
        df = pd.read_csv('../scraping/data/lyrics/' + filename)
        if len(df) < 7:
            continue
        # slide window of length 7 across dataset
        # preprocess and append each group of 7 lines to 'data'
        # pad so each line has length of 15
        context_temp = deque([[''] * 15,[''] * 15,[''] * 15])
        for index, row in df.iterrows():
            line = re.sub('[^a-z0-9\\s]', '', str(row['line']).lower()).split(' ')
            if len(line) >= 15:
                line = line[:15]
            else:
                line.extend([''] * (15 - len(line)))
            label = int(row['annotated'])
            
            if index < 3:
                context_temp.append(line)
                labels.append(label)
            else:
                context_temp.append(line)
                labels.append(label)
                data.append(np.array(get_array_from_deque(context_temp)))
                context_temp.popleft()

        for i in range(3):
            context_temp.append([''] * 15)
            data.append(np.array(get_array_from_deque(context_temp)))
            context_temp.popleft()
            
    # convert data to numpy array
    data_array = np.array(data)
    label_array = np.array(labels)
    
    # perform train-val-test split
    X_train, X_temp, y_train, y_temp = train_test_split(
            data_array, label_array, test_size=0.10, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=42)
    
    np.save('training_data/X_train.npy', X_train)
    np.save('training_data/y_train.npy', y_train)
    np.save('training_data/X_val.npy', X_val)
    np.save('training_data/y_val.npy', y_val)
    np.save('training_data/X_test.npy', X_test)
    np.save('training_data/y_test.npy', y_test)
            
