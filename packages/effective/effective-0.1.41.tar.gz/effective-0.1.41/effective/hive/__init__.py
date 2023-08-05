#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File Name: __init__.py
    Author: HuHao
    Mail: whohow20094702@163.com
    Created Time:  '2019/2/28 20:48:00'
    Info: A effective style to operate sql
          Support for HA-connection, retry-support, high-tolerance params, self-batch execution
    Licence: GPL Licence
    Url: https://github.com/GitHuHao/effective.git
    Version: 0.1.10
"""
import sys
from pyhive import hive
# pip install sasl thrift thrift-sasl
import time, traceback
import logging
from pprint import pprint as ppt

version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib
    importlib.reload(sys)

class HiveSQL:

    def __init__(self, kwargs=None):
        '''
        :param kwargs:
            mondary: host, user, passwd, db, port, charset
            potational:
                connect_timeout=60s,
                cursor_type (eg:Cursor\SSCursor\DictCursor\SSDictCursor)
                execute_retries 查询重试次数 3
                fail_sleep 重刷间隔 3
                settings=('SET names utf8',)
                setsession=self.settings,  # SET 配置操作集合，诸如：["set datestyle to ...", "set time zone ...","set autocommit 0","set name UTF-8"],
                loglevel='DEBUG|INFO|ERROR'
        '''
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 3306)
        self.user = kwargs.get('user', 'root')
        self.passwd = kwargs.get('passwd', 'root')
        self.db = kwargs.get('db', 'test')
        self.charset = kwargs.get('charset', 'utf8')
        self.cursor_key = kwargs.get('cursor_type', 'DictCursor')
        self.execute_retries = kwargs.get('execute_retries', 60)
        self.fail_sleep = kwargs.get('fail_sleep', 3)
        self.setting_map = dict()
        self.setting_map.update(**kwargs.get('settings', dict()))
        self.is_debug =  kwargs.get('is_debug', False)
        self.loglevel = kwargs.get('loglevel', 'DEBUG')

        logging.basicConfig(
            format='%(asctime)s [%(filename)30s %(funcName)30s line:%(lineno)3d] %(levelname)7s: %(message)s' if self.is_debug
                    else '%(asctime)s [line:%(lineno)3d] %(levelname)7s: %(message)s',
            level=getattr(logging, self.loglevel)
        )
        self.logger = logging

        self.escaper = hive.HiveParamEscaper()

    def add_logger(self, logger):
        self.logger = logger
        return self

    def _conn(self):
        '''
        初始化连接
        :return:
        '''
        try:
            self.conn = hive.connect(host=self.host, port=self.port, username=self.user, database=self.db, configuration=self.setting_map)
            self.cursor = self.conn.cursor()
            for k,v in self.setting_map.iteritems():
                self.logger.debug('SET %s=%s;' %(k,v))
            self.logger.info('Init HIVE DB(%s)' % self.db)
            return True
        except:
            return False

    def ping(self):
        self.cursor.execute("show databases")
        self.cursor.fetchall()

    def _reConn(self):
        '''
        维持长连接
        :return:
        '''
        retries = 1
        while True:
            try:
                if getattr(self,'conn',None) is None:
                    self._conn()
                self.ping()
                break
            except Exception as e:
                self.logger.error(
                    '%d time fail for (%s), sleep for %d seconds.' % (retries, ', '.join(['%s'%x for x in e.args]),self.fail_sleep)
                )
                if self._conn() == True:
                    break
                retries += 1
                if retries > self.execute_retries:
                    raise e
                else:
                    time.sleep(self.fail_sleep)

    def close(self):
        '''
        关闭连接池
        :return:
        '''
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.conn is not None:
                self.conn.close()
        except:
            pass
        finally:
            self.logger.info('Close %s connection' % self.db)

    def _atomic_action(self, sql, params):
        retries = 0
        while True:
            try:
                self._reConn()
                self.cursor.execute(sql, params)
                result = self.cursor.fetchall()
                if self.cursor_key =='DictCursor':
                    columns = [x[0].split('.')[-1] for x in self.cursor.description]
                    tmp = []
                    for row in result[1:]:
                        jrow = dict()
                        jrow.update(zip(columns,row))
                        tmp.append(jrow)
                    result = tmp
                else:
                    result = result[1:]
                break
            except Exception as e:
                self.logger.error('(%s)' % (', '.join(['%s'%x for x in e.args])))
                retries += 1
                if retries == self.execute_retries:
                    raise e
                else:
                    time.sleep(self.fail_sleep)
        return result

    def _batch_action(self, sql, params, batch, pojo):
        '''
        self.cursor.execute("SET GLOBAL max_allowed_packet=1024*1024*1024")
        :param sql:
        :param params: tuple、multi-array、dict、dict-list
        :param batch:  single thread processing batch
        :return: the effected lines.
        '''

        self.logger.debug(sql % self.escaper.escape_args(params))

        result = self._atomic_action(sql, params)
        self.logger.debug("FETCH %s ROWS ." % len(result))

        if pojo is not None:
            if isinstance(result[0], dict):
                result = [pojo(**res) for res in result]
            else:
                result = [pojo(*res) for res in result]
            self.logger.debug("WRAPPER %s ROWS ." % len(result))

        return result

    def fly(self,
            sql,  # crud 、 upsert sql or dataframe
            params=None,  # tuple、multi-array、pojo-list、dict、dict-list、Nothing
            pojo=None,  # pojo class
            fields=None,  # fields name of pojo which will be use
            batch=1024,  # single thread batch
            propagation=True
            ):
        '''
        :param sql:
            my.fly('select * from car where id=100')
            my.fly('select * from car where id=%s',params=(100L,))
            my.fly('select * from car where id=%(id)s', param_dict={'id':100L})
        :param params: 元组
        :param param_dict: 字典
        :param option: 操作 SqlOption.Query、SqlOption.Execute
        :param propagate: 是否抛出异常
        :return: (成功与否,影响行数 或 抓取数据集)
        '''
        self._reConn()
        try:
            if params is None:
                params = dict()

            result = self._batch_action(sql, params, batch, pojo)
            success = True
            return (success, result)
        except Exception as e:
            if propagation:
                raise e

    def api(self):
        self.usage = '''
        You can call like these :
        注意：插入语句如果带主键，主键自增，会导出冲突问题）
        1) CRUD 传参兼容 
            # query 直接传单参
            status,result =my.fly('select * from car where name="A100"')
            print(status,result)

            query 直接传单参
            print(my.fly('select * from car where price>1900'))
            print(status,result)

            # query 错误传参 兼容值 （顺便封装对象）
            status,result = my.fly('select name,price,id from car where name=%s',params="A100",pojo=Car)
            print(status,result)

            # query 错误传参 兼容 dict（顺便封装对象）
            status,result = my.fly('select price,id,name from car where name=%(name)s',params={'name':'A100'},pojo=Car)
            print(status,result)

            # query 错误传参 兼容 ('A100',) 和 ('A100') （顺便封装对象）
            status,result = my.fly('select price,id,name from car where name=%s',params=('A100',),pojo=Car)
            print(status,result)

        2）BATCH EXECUTE
            # execute insert update select delete （顺便封装对象）
            print(my.fly('insert into car(price,name) values (%s,%s)',params=(2500L,'A100')))
            print(my.fly('update car set price=%s where name=%s and price=%s', params=(1000,'A100',2500L)))
            print(my.fly('select price,id,name from car where name=%(name)s', params={'name': 'A100'}, pojo=Car)[1])
            print(my.fly('delete from car where name=%s',params='A100'))
            print(my.fly('select price,id,name from car where name=%(name)s', params={'name': 'A100'}, pojo=Car))

            # batch tuple insert
            params = [('A%s' % i, i) for i in range(1,1000000)]
            status, count = my.fly(sql='insert into car(name,price) values (%s,%s)', params=params)
            print(status, count)

            # batch dict insert
            param_dict = [{'id': i, 'name': 'A%s' % i, 'price': i} for i in range(1, 10000)]
            status, count = my.fly(sql='insert into car(name,price) values (%(name)s,%(price)s)', params=param_dict)
            print(status, count)

            # batch instance insert
            instances = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 100000)]
            rows = my.fly(sql='insert into car(name,price) values (%s,%s)', params=instances, fields=['name','price'])
            print(rows)

            # batch instance delete 兼容 fields 异常传参
            instances = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 2000)]
            rows = my.fly(sql='delete from car where name =%s', params=instances, fields='name')
            print(rows)

            # batch instance upsert
            instances = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 4000)]
            rows = my.fly(sql='INSERT INTO car(name,price) VALUES (%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name)',
                          params=instances, fields=['name', 'price'])
            print(rows)

        3)  BEST PRACTICE
            db.yaml
            -----------------------------------------------------------------------------
            # 数据库连接
            database:
              # 线上运行环境
              online:
                hybridb:
                  host: xxxxx
                  port: 3306
                  db: xxxx
                  user: xxxx
                  passwd: xxxx
                  cursor_type: DictCursor
                  loglevel: INFO

              # 线下编码环境
              offline:
                hybridb:
                  host: xxxxx
                  port: 3306
                  db: xxxxx
                  user: xxxxx
                  passwd: xxxxx
                  cursor_type: DictCursor
                  loglevel: DEBUG
            -----------------------------------------------------------------------------

            init.sql
            -----------------------------------------------------------------------------
            CREATE TABLE `car` (
              `id` int(3) NOT NULL AUTO_INCREMENT,
              `name` varchar(50) DEFAULT NULL,
              `price` bigint(5) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=2000 DEFAULT CHARSET=utf8;
            -----------------------------------------------------------------------------

            best-practice.py
            -----------------------------------------------------------------------------
            import sys,os
            from effective_sql import MySQL

            ENV = 'online' if sys.platform != 'darwin' else 'offline'

            class Car:
                def __init__(self,price,id,name):
                    self.price = price
                    self.id = id
                    self.name = name

                def __str__(self):
                    return 'Car: id=%s, price=%s, name=%s'%(self.id,self.price,self.name)

                def __repr__(self):
                    return 'Car: id=%s, price=%s, name=%s'%(self.id,self.price,self.name)

            def get_section(yml,*args):
                if os.path.exists(yml):
                    with open(yml, "r") as file:
                        config = yaml.load(file)
                    recursive = 0
                    while recursive < len(args):
                        config = config[args[recursive]]
                        recursive += 1
                    return config
                else:
                    raise RuntimeError("%s not exists"%yml)

            conf = get_section('db.yaml','database', ENV,'hybridb')
            client = MySQL(conf)

            cars = [Car(price=i,name='A%s' % i, id=i) for i in range(0, 100000)]
            success,rows = client.fly(
                sql='INSERT INTO car(name,price) VALUES (%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name)',
                params=cars, fields=['name', 'price']
                )
            if success: print(rows)

            success,cars = client.fly(
                sql='select * from car where price>%s and price<%s',
                params=(1500,300),
                pojo=Car
            )
            if success: print(rows)
            -----------------------------------------------------------------------------

        End
        '''

        ppt(self.usage.replace('        ', '').decode('utf-8'))

