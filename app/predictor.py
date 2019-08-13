import pickle
import numpy as np

from keras.models import load_model

from model.embedding_utils import embed_inputs_for_embedding_layer


class Predictor():
    def __init__(self):
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()

    def load_tokenizer(self):
        with open('model/final/tokenizer_mini.pkl', 'rb') as f:
            tk = pickle.load(f)
        return tk

    def load_model(self):
        return load_model('model/final/model_mini.h5')

    def test(self, request):
        return request.method

    def predict(self, request):
        return request.method
