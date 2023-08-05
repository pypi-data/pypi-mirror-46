#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2019/3/3'
Info:

"""
import pandas as pd
# pip2.7 install PTable
import sys
from prettytable import PrettyTable
from pandas import Series

version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib
    importlib.reload(sys)

def tabstring(df, name):
    '''
    表格化
    :param df:
    :param name:
    :return:
    '''
    if type(df) == Series:
        df = df.to_frame()

    tab = PrettyTable()
    tab.padding_width = 1
    tab.title = name

    # 设置表头
    field_names = [' ']
    field_names.extend(df.columns)
    tab.field_names = field_names
    indexs = df.index.values

    # 表格内容插入
    values = df.values
    for i in range(len(values)):
        tmp = [indexs[i]]
        tmp.extend(values[i])
        tab.add_row(tmp)

    tab_info = str(tab)

    return '\n%s' % tab_info

# if __name__=='__main__':
#     from pandas import DataFrame
#
#     df = DataFrame([{'amount': 10, 'price': 0.1, 'money': 1}, {'amount': 20, 'price': 0.2, 'money': 4},
#                     {'amount': 30, 'price': 0.3, 'money': 9}]).T
#     print(tabstring(df,'aaa'))