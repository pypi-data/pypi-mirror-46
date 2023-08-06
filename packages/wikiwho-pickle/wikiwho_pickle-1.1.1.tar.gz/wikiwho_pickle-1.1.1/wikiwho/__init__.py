from . import structures
from . import wikiwho_simple

from os.path import join
from os import makedirs
import pickle


def open_pickle(article_id, pickle_path='pickles', lang=''):
    with open(join(pickle_path, lang, f'{article_id}.p'), 'rb') as _f:
        return pickle.load(_f)
