#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'SparkInit'
__author__ = 'JieYuan'
__mtime__ = '2019-05-13'
"""

import pyspark.sql.functions as F
from pyspark.sql import *
from pyspark.sql.types import *


class SparkInit(object):

    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Yuanjie") \
            .config('log4j.rootCategory', "WARN") \
            .enableHiveSupport() \
            .getOrCreate()

        self.sc = self.spark.sparkContext
        print(self.spark.version)

    def __call__(self, *args, **kwargs):
        return self.sc, self.spark

sc, spark = SparkInit()()