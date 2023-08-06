#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

__name__ = 'pflogger'
__version__ = '1.0.0'
__author__ = 'ClaireHuang'
__author_email__ = 'clairehf@163.com'


MAX_BYTES = int(os.environ.get('_LOG_MAX_BYTES', '52428800'))
BACKUP_COUNT = int(os.environ.get('_LOG_BACKUP_COUNT', '10'))

LOG_FORMAT = "%(asctime)s | %(levelname)-10s [%(filename)s:%(lineno)d(%(" \
             "funcName)s)] %(message)s"


def init_logging(log_level, file_name="/var/log/root.log"):
    logging.basicConfig(level=log_level, format=LOG_FORMAT)
    handler = RotatingFileHandler(file_name, maxBytes=MAX_BYTES,
                                  backupCount=BACKUP_COUNT)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logging.getLogger().addHandler(handler)