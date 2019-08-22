import pickle
import re
import numpy as np
import pandas as pd
from collections import deque
from keras.models import load_model

from model.embedding_utils import embed_inputs_for_embedding_layer


class Predictor():
    def __init__(self):
        self.tk = self.load_tokenizer()
        self.model = self.load_model()
        self.model._make_predict_function()
        return None

    def load_tokenizer(self):
        with open('app/model/tokenizer_mini.pkl', 'rb') as f:
            tk = pickle.load(f)
        return tk

    def load_model(self):
        return load_model('app/model/model_mini.h5')

    def get_array_from_deque(self, queue):
        temp = []
        for entry in queue:
            temp.extend(entry)
        return temp

    def embed_inputs(self, data_array, tk):
        word_to_int = tk.word_index
        data_embedded = []

        for sample in data_array:
            data_embedded_temp = []
            for word in sample:
                index = 0 if word not in word_to_int else word_to_int[word]
                data_embedded_temp.append(index if index < 6000 else 0)
            data_embedded.append(np.array(data_embedded_temp))
        return np.array(data_embedded)


    def preprocess_lines(self, split_lines):
        data = []
        df = pd.DataFrame(split_lines)
        df.columns = ['lyric']
        context_temp = deque([[''] * 15,[''] * 15,[''] * 15])
        for index, row in df.iterrows():
            line = re.sub('[^a-z0-9\\s]', '', str(row['lyric']).lower()).split(' ')
            if len(line) >= 15:
                line = line[:15]
            else:
                line.extend([''] * (15 - len(line)))
            if index < 3:
                context_temp.append(line)
            else:
                context_temp.append(line)
                data.append(np.array(self.get_array_from_deque(context_temp)))
                context_temp.popleft()

        for i in range(3):
            context_temp.append([''] * 15)
            data.append(np.array(self.get_array_from_deque(context_temp)))
            context_temp.popleft()

    # convert data to numpy array
        data_array = np.array(data)
        return data_array

    def test(self, request):
        return request.method

    def predict(self, request):
        print(request)
        req_data = request.form['lyrics']
        split_lines = req_data.splitlines()
        data_array = self.preprocess_lines(split_lines)
        data_embedded = self.embed_inputs(data_array, self.tk)
        print(split_lines)
        print(data_array)
        print(data_embedded)
        predictions = self.model.predict(data_embedded)
        print(predictions)
        return'''Line 2: {}  <br> Tokenized Input: {} <br> Prediction: {} <br><br>
                 Line 5: {}  <br> Tokenized Input: {} <br> Prediction: {}'''.format(split_lines[1], data_array[1], predictions[1], split_lines[4], data_array[4], predictions[4])
