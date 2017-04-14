# -*- coding: utf-8 -*-
import utils
import json

from keras.preprocessing import sequence

from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import GRU, LSTM
from keras.layers.core import Dense, Dropout

resources = 'resources/'
cases = {'bank':
             {'train': {'file': resources + 'bank_train_2016.xml', 'n': 8},
              'json_train': resources + 'bank_train.json',
              'etalon': {'file': resources + 'banks_test_etalon.xml', 'n': 8},
              'json_etalon': resources + 'bank_etalon.json'},
         'tkk':
             {'train': {'file': resources + 'tkk_train_2016.xml', 'n': 7},
              'json_train': resources + 'tkk_train.json',
              'etalon': {'file': resources + 'tkk_test_etalon.xml', 'n': 7},
              'json_etalon': resources + 'tkk_etalon.json'}
         }
output = resources+'output.xml'


def make_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def serialize_data(plain_data_tuple, json_file):
    """
    Приготовление данных из xml долгий процесс, поэтому заводитятся json для готовых данных
    """
    twits, emotions, weight = utils.load_train_data(plain_data_tuple['file'], plain_data_tuple['n'])
    make_json({"twits": twits, "emotions": emotions, "weight": weight}, json_file)


def load_data(json_file):
    """
    Загрузка приготовленных данных из json
    """
    with open(json_file) as data:
        data = json.loads(data.read())
    twits = data["twits"]
    emotions = data["emotions"]
    weight_json = data["weight"]
    weight = {0: weight_json['0'], 1: weight_json['1'], 2: weight_json['2']}
    return twits, emotions, weight


if __name__ == "__main__":
    case = cases['tkk']
    # run once to create jsons with prepared data
    # serialize_data(case['train'], case['json_train'])
    # serialize_data(case['train'], case['json_etalon'])
    # serialize_data(case['train'], case['json_train'])
    # serialize_data(case['train'], case['json_etalon'])
    train_twits, train_emotions, train_weight = load_data(case['json_train'])
    test_twits, test_emotions, test_weight = load_data(case['json_etalon'])
    max_length = max([len(s) for s in train_twits + test_twits])
    vocabulary = utils.make_vocabulary(train_twits+test_twits)
    X_train = sequence.pad_sequences(utils.convert_twits_data(train_twits, vocabulary), maxlen=max_length)
    X_test = sequence.pad_sequences(utils.convert_twits_data(test_twits, vocabulary), maxlen=max_length)
    y_train = utils.convert_val_data(train_emotions)
    y_test = utils.convert_val_data(test_emotions)

    network = Sequential()
    network.add(Embedding(input_dim=len(vocabulary) + 1, output_dim=64,
                          input_length=max_length, mask_zero=True))
    # 1network.add(GRU(units=64))
    # 2network.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
    network.add(LSTM(64))
    # 3network.add(LSTM(64, return_sequences=True))
    # 3network.add(LSTM(64))
    network.add(Dropout(rate=0.5))
    network.add(Dense(units=3, activation="softmax"))
    network.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    network.fit(X_train, y_train, verbose=1, batch_size=8, epochs=3,
                class_weight=train_weight, validation_split=0.0, validation_data=(X_test, y_test))

    test_emotions = network.predict_classes(X_test, batch_size=1)
    utils.emotions_to_xml(case['etalon'], output, test_emotions)
