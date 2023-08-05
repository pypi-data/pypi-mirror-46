#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2019/3/11'
Info:

"""
import sys

import datetime, time, pytz

version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib
    importlib.reload(sys)

class DateTime:
    def __init__(self,obj=None,string=None,tmstp=None,ifmt='%Y-%m-%d %H:%M:%S',ofmt='%Y-%m-%d %H:%M:%S',
                 tzinfo=pytz.timezone('Asia/Shanghai')):
        if obj is None:
            obj=datetime.datetime.now()
        if string is not None:
            obj = datetime.datetime.strptime(string, ifmt)
        elif tmstp is not None:
            obj = datetime.datetime.strptime(time.strftime(ofmt, time.localtime(float(str(tmstp)))), ofmt)

        self.tzinfo = tzinfo
        self.tmstp = int(time.mktime(obj.timetuple()))
        self.obj = datetime.datetime(obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second, tzinfo=tzinfo)
        self.string = obj.strftime(ofmt)

    def window(self, seconds, ifmt='%Y-%m-%d %H:%M:%S', ofmt='%Y-%m-%d %H:%M:%S'):
        if round(seconds) != 0:
            cnt = self.tmstp / abs(seconds*1.0)
            start_tmstp = (abs(seconds) * cnt)
            end_tmstp = (abs(seconds) * (cnt-1 if seconds < 0 else cnt+1))
            start = DateTime(tmstp=min(start_tmstp,end_tmstp),ifmt=ifmt,ofmt=ofmt,tzinfo=self.tzinfo)
            end = DateTime(tmstp=max(start_tmstp,end_tmstp),ifmt=ifmt,ofmt=ofmt,tzinfo=self.tzinfo)
        else:
            start,end = (self, self)
        return (start, end)

    @staticmethod
    def range(startstring, endsting,seconds,include=True,ifmt='%Y-%m-%d %H:%M:%S',ofmt='%Y-%m-%d %H:%M:%S',
              tzinfo=pytz.timezone('Asia/Shanghai')):
        seconds = abs(seconds)
        now = DateTime(obj=None,ifmt=ifmt, ofmt=ifmt, tzinfo=tzinfo)

        startstr = now.string if startstring is None else startstring
        start = DateTime(string=startstr, ifmt=ifmt, ofmt=ofmt, tzinfo=tzinfo)

        stopstr = now.string if endsting is None else endsting
        stop = DateTime(string=stopstr, ifmt=ifmt, ofmt=ofmt, tzinfo=tzinfo)

        if include:
            opt, idx, step = ('>', 1, seconds) if startstr <= stopstr else ('<', 0, -seconds)
        else:
            opt, idx, step = ('>=', 1, seconds) if startstr < stopstr else ('<', 0, -seconds)

        while True:
            if eval('start.string %s stop.string' % opt):break
            yield start
            if endsting is None:
                stop = DateTime(obj=None, ifmt=ifmt, ofmt=ofmt, tzinfo=tzinfo)
            if eval('start.string %s stop.string' % opt):break
            start = start.window(step, ifmt=ifmt, ofmt=ofmt)[idx]

    def __str__(self):
        return 'DateTime:[string:%s, tmstp:%s, obj:%s]' % (self.string,self.tmstp,self.obj)

    def __repr__(self):
        return 'DateTime:[string:%s, tmstp:%s, obj:%s]' % (self.string,self.tmstp,self.obj)


if __name__ == '__main__':
    # dt1 = DateTime(string="2019-01-02 00:00:00")
    # print(dt1)
    # print(dt1.window(seconds=-15*60))
    # print(dt1.window(seconds=24 * 60 * 60))

    # for d in DateTime.range(startstring='2019/03/31',endsting=None,seconds=24*60*60,include=True,ifmt='%Y/%m/%d',ofmt='%Y-%m-%d'):
    #     print(d)

    # for d in DateTime.range(startstring='2019/03/31',endsting=None,seconds=24*60*60,include=False,ifmt='%Y/%m/%d',ofmt='%Y-%m-%d'):
    #     print(d)

    # for d in DateTime.range(startstring='2019/04/06',endsting='2019/03/31',seconds=24*60*60,include=False,ifmt='%Y/%m/%d',ofmt='%Y-%m-%d'):
    #     print(d)

    for d in DateTime.range(startstring='2019/03/31', endsting=None, seconds=24 * 60 * 60, include=False,ifmt='%Y/%m/%d', ofmt='%Y-%m-%d'):
        print(d)



    pass
