#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/05/08 18:56
# @Author  : niuliangtao
# @Site    : 
# @File    : ItemUtils.py
# @Software: PyCharm


import json
import logging
from urllib import request

logger = logging.getLogger('ItemUtils')

__all__=['fill_item_info']


def fill_item_info(item_list=None):
    if item_list is None or not isinstance(item_list,list):
        raise Exception('入参 item_list 是list')
    items = ','.join(item_list)
    url = 'http://pluto.vdian.net/solution/query?solutionId=1004&itemIdList=' + items
    logger.debug('url:' + url)

    f = request.urlopen(url)

    response = json.loads(f.read())

    logger.debug('response:' + str(response))
    result = response['result']['result']
    
    return result

