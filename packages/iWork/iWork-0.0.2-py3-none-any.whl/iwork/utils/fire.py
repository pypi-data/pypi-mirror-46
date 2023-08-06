#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'fire'
__author__ = 'JieYuan'
__mtime__ = '19-1-10'
"""

import fire


class Config(object):
    x = 1
    y = 1


opt = Config()


class G:
    @staticmethod
    def gen(**kwargs):
        for i in kwargs.items():
            setattr(opt, *i)

        return opt.x + opt.y


gen = G.gen
if __name__ == '__main__':
    fire.Fire()
