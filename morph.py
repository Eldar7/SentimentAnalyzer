# -*- coding: utf-8 -*-
from pymorphy2 import MorphAnalyzer
import string
from pymorphy2.tokenizers import simple_word_tokenize
import re

morph = MorphAnalyzer()
stopwords = set(string.punctuation) | {u'–', u'-', u'—', u'…', u'«', u'»', u'“', u'”'}


def normalized(twit):
    twit = re.sub(r'#\S+', '', #вычищение хештегов
                  re.sub(r'@\S+', '', #вычищение @name
                         re.sub(r'http\S+', '', #вычищение ссылок
                                re.sub(r'RT ', '', #убрать RT
                                       re.sub("\d+", "", twit)))) #убираем все цифры
                  ).strip()
    tokens = simple_word_tokenize(twit)
    parses = [
        morph.parse(w)[0]
        for w in tokens
        if w.lower() not in stopwords
    ]
    parses = [
        p for p in parses
        if p.tag.POS not in {'PNCT', 'UNKN', 'NUMB', 'CONJ', 'LATN'}
    ]
    return [p.normal_form.lower() for p in parses]
