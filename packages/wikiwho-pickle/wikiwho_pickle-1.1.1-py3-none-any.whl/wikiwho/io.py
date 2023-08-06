from os.path import join
from os import makedirs
import pickle


class WikiWhoPickle():

    def __init__(self, path='pickles', lang=''):
        self.path = join(path, lang)
        try:
            makedirs(self.path)
        except FileExistsError:
            pass

    def open_pickle(self, article_id):
        with open(join(self.path, f'{article_id}.p'), 'rb') as _f:
            return pickle.load(_f)
