#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'nms'
__author__ = 'JieYuan'
__mtime__ = '2019-05-14'
"""
# import nmslib
# import numpy
#
# # create a random matrix to index
# data = numpy.random.randn(1000, 100).astype(numpy.float32)
#
# # initialize a new index, using a HNSW index on Cosine Similarity
# index = nmslib.init(method='hnsw', space='cosinesimil')
# index.addDataPointBatch(data)
# index.createIndex({'post': 2}, print_progress=True)
#
# # query for the nearest neighbours of the first datapoint
# ids, distances = index.knnQuery(data[0], k=10)
#
# # get all nearest neighbours for all the datapoint
# # using a pool of 4 threads to compute
# neighbours = index.knnQueryBatch(data, k=10, num_threads=4)