#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2019/4/6'
Info:
        
"""

import os, sys

# import start
import yaml


# import end
version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib

    importlib.reload(sys)

def get_conf(yml):
    if os.path.exists(yml):
        with open(yml,"r") as file:
            config = yaml.safe_load(file)
        return config
    else:
        raise RuntimeError("%s not exists" % yml)

def get_section(yml,*args):
    if os.path.exists(yml):
        with open(yml, "r") as file:
            config = yaml.safe_load(file)
        recursive = 0
        while recursive < len(args):
            config = config[args[recursive]]
            recursive += 1
        return config
    else:
        raise RuntimeError("%s not exists"%yml)
