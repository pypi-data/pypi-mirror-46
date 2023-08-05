#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: HuHao <huhao1@cmcm.com>
Date: '2019/2/26'
Info:

"""

import os, sys
import errno
import logging
import multiprocessing
from logging.handlers import RotatingFileHandler

version = sys.version_info.major
if version == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    import importlib

    importlib.reload(sys)


class SafeRotatingFileHandler(RotatingFileHandler):
    """
    多进程下 RotatingFileHandler 会出现问题
    """

    _rollover_lock = multiprocessing.Lock()

    # noinspection PyBroadException
    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.shouldRollover(record):
                with self._rollover_lock:
                    if self.shouldRollover(record):
                        self.doRollover()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def shouldRollover(self, record):
        if self._should_rollover():
            # if some other process already did the rollover we might
            # checked log.1, so we reopen the stream and check again on
            # the right log file
            if self.stream:
                self.stream.close()
                self.stream = self._open()

            return self._should_rollover()

        return 0

    def _should_rollover(self):
        if self.maxBytes > 0:
            if self.stream:
                self.stream.seek(0, 2)
                if self.stream.tell() >= self.maxBytes:
                    return True

        return False


def get_logger(log_dir='../log', name=None, maxBytes=50 * 1024 * 1024, backupCount=5,
               fmt='default', datefmt='%Y-%m-%d %H:%M:%S %p', level='DEBUG', is_debug=False):
    """
    :param log_dir: log file dir
    :param name: logger name
    """
    level = eval('logging.%s' % level.upper())

    ifmt = '%(asctime)s [%(filename)30s %(funcName)30s line:%(lineno)3d] %(levelname)7s: %(message)s' if is_debug \
        else '%(asctime)s [line:%(lineno)3d] %(levelname)7s: %(message)s'

    if fmt == 'default':
        fmt = ifmt

    log_formater = logging.Formatter(fmt=fmt, datefmt=datefmt)

    try:
        os.makedirs(log_dir)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(log_dir):
            pass
        else:
            raise

    _logger = logging.getLogger(name)
    _logger.propagate = False

    _logger.setLevel(level)

    hdlr = logging.StreamHandler()
    hdlr.setLevel(level)
    hdlr.setFormatter(log_formater)
    _logger.addHandler(hdlr)

    filename = "root.log" if name is None else "%s.log" % name
    hdlr = SafeRotatingFileHandler(
        os.path.join(log_dir, filename),
        maxBytes=maxBytes, backupCount=backupCount
    )
    hdlr.setFormatter(log_formater)
    _logger.addHandler(hdlr)

    return _logger


if __name__ == '__main__':
    logger = get_logger()
    logger.info('test')