#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'demo'
__author__ = 'JieYuan'
__mtime__ = '2019-04-30'
"""

import requests


def request(url, params=None):
    try:
        # headers：伪装spider
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        }
        headers = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, params, headers=headers)
        r.raise_for_status()  # 申请返回的状态码: 200为成功
        r.encoding = r.apparent_encoding
        print(r.text.split()[:32])
        return r

    except Exception as e:
        print('爬取失败：%s' % e)


if __name__ == '__main__':
    request('https://www.baidu.com/s?wd=周杰伦')
    request('https://www.baidu.com/s', {'wd': '周杰伦'})
