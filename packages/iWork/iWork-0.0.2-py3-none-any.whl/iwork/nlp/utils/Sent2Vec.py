import numpy as np
from tqdm import tqdm

"""
1. 加和/平均
2. Concatenated p-mean Word Embeddings: https://blog.csdn.net/triplemeng/article/details/81298100
3. InferSent: https://github.com/facebookresearch/InferSent
"""


class Sent2Vec(object):

    def __init__(self, fname):
        self.embeddings = {}
        self.word_size = None
        self._load_wv(fname)

    def sent2vec(self, sentence, tokenizer=str.split, mode='sum', normalize=False):
        words = [w for w in tokenizer(sentence) if w in self.embeddings]

        if words:
            if mode == 'sum':
                _ = np.array([self.embeddings[w] for w in words]).sum(axis=0)
                return _ / np.sqrt(np.clip((_ ** 2).sum(), 1e-12, None)) if normalize else _
            elif mode == 'mean':
                _ = np.array([self.embeddings[w] for w in words]).mean(axis=0)
                return _ / np.sqrt(np.clip((_ ** 2).sum(), 1e-12, None)) if normalize else _
            else:
                return np.zeros(self.word_size)
        else:
            return np.zeros(self.word_size)

    def _load_wv(self, fname):
        with open(fname) as f:
            for line in tqdm(f, 'Load Vectors ...'):
                line = line.strip().split()
                if len(line) > 2:
                    self.embeddings[line[0]] = np.asarray(line[1:], dtype='float32')
            self.word_size = len(line[1:])
