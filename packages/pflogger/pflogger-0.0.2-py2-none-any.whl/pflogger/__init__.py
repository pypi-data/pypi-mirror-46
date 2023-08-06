#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

__name__ = 'pflogger'
__version__ = '0.0.2'
__author__ = 'ClaireHuang'
__author_email__ = 'clairehf@163.com'


MAX_BYTES = int(os.environ.get('_LOG_MAX_BYTES', '52428800'))
BACKUP_COUNT = int(os.environ.get('_LOG_BACKUP_COUNT', '10'))

LOG_FORMAT = "%(asctime)s | %(levelname)-10s [%(filename)s:%(lineno)d(%(" \
             "funcName)s)] %(message)s"


class MyLoggerHandler(logging.Logger):
    def __init__(self, name="root"):
        self.name = name
        self.filename = "/var/log/" + name + ".log"
        logging.Logger.__init__(self, self.name)

    def set_logfile(self, filename):
        self.filename = filename

    def set_myhandler(self, level="DEBUG"):
        handler = RotatingFileHandler(self.filename, maxBytes=MAX_BYTES,
                                      backupCount=BACKUP_COUNT)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        self.addHandler(handler)


mylogger = MyLoggerHandler()