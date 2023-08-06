# #!/usr/bin/env python
# #-*- coding: utf-8 -*-
# """
# __title__ = 'IndexQuery'
# __author__ = 'JieYuan'
# __mtime__ = '2019-05-14'
# """
# import numpy
# import gensim
# import nmslib


class IndexQuery(object):

    def __init__(self):
        self.model = gensim.models.fasttext.load_facebook_model('../Data/WordVector/cbow.title')
        self.index = nmslib.init(method='hnsw', space='cosinesimil')
        self.index.addDataPointBatch(self.model.wv.vectors)
        self.index.createIndex({'post': 2})
        id2word = dict(enumerate(self.model.wv.index2entity))
        word2id = {j: i for i, j in id2word.items()}

    def get(self, sent):
        v = model.wv[sent]
        ids, distances = index.knnQuery(v, k=10)
        # l = index.knnQueryBatch(data[:2], k=10, num_threads=4)
        for i in ids:
            print(self.model.wv.index2entity[i])
