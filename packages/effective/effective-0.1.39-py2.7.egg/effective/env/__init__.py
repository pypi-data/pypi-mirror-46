#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2019/2/26'
Info:

"""
import sys, os

version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib
    importlib.reload(sys)

# 环境
ENV = 'online' if sys.platform != 'darwin' else 'offline'

def get_env(key):
    '''
    获取shell环境变量
    :param key:
    :return:
    '''
    os.os.putenv()
    return os.os.getenv(key, None)

def set_env(key,value):
    '''
    设置shell环境变量
    :param key:
    :return:
    '''
    os.os.putenv(key,value)

def unset_env(key):
    '''
    设置shell环境变量
    :param key:
    :return:
    '''
    os.os.unsetenv(key)

__all__ = ['ENV', 'get_env']