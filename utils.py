# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import morph
import numpy as np


def get_emotion(node, n_positions):
    emotion = 0
    for elem in node[4:4+n_positions]:
        if elem.text != u"NULL" and elem.text != 0:
            emotion = int(elem.text) + 1
    return emotion


def load_train_data(filename, n_positions):
    train_twits = []
    train_emotions = []
    root = ET.parse(filename).getroot()
    for node in root[1]:
        train_emotions.append(get_emotion(node, n_positions))
        train_twits.append(morph.normalized(node[3].text))
    negative = train_emotions.count(0)
    neutral = train_emotions.count(1)
    positive = train_emotions.count(2)
    class_weight = {0: float(neutral) / negative, 1: 1.0, 2: float(neutral) / positive}
    return train_twits, train_emotions, class_weight


def load_test_data(filename):
    test_twits = []
    root = ET.parse(filename).getroot()
    for node in root[1]:
        test_twits.append(morph.normalized(node[3].text))
    return test_twits


def emotions_to_xml(input_tuple, output, emotions):
    root = ET.parse(input_tuple['file']).getroot()
    for node in enumerate(root[1]):
        for elem in node[1][4:4+input_tuple['n']]:
            if elem.text != u"NULL":
                elem.text = str(emotions[node[0]]-1)
    with open(output, "w") as text_file:
        text_file.write(tostring(root))
    print (output, ' saved.')


def make_vocabulary(twits):
    words = set()
    for twit in twits:
        for token in twit:
            words.add(token)
    # словарь начинаем с 1, 0 для выравнивания длины твитов
    vocabulary = {k: v + 1 for v, k in enumerate(list(words))}
    return vocabulary


def convert_twits_data(data, vocabulary):
    train_data = list()
    for twit in data:
        coded_twit = [vocabulary[w] for w in twit]
        train_data.append(coded_twit)
    return train_data


def convert_val_data(val_data):
    def convert_emotion(emotion):
        """
        Преобразует скалярную эмоцию из {0,1,2} в вектор с сединицей
        в соответствующей позиции
        :param emotion: скалярная эмоция из {0,1,2}
        :return: вектор длины 3 с единицей в позиции соовтветствующей emotion
        """
        vec_emotion = np.zeros(3)
        vec_emotion[emotion] = 1
        return vec_emotion
    return np.asarray([convert_emotion(e) for e in val_data])


