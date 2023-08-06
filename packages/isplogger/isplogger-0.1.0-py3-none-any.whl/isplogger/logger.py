#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isplogger/logger.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Console/text file logging
#

import logging
import datetime
import os


_MSG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
_FILE_FORMAT = '{}.log'.format(datetime.datetime.now().strftime(
    '%Y%m%d%H%M%S'
))
LOGGER = logging.getLogger('down_detector')
__stream_handler = logging.StreamHandler()
__stream_handler.setFormatter(logging.Formatter(
    _MSG_FORMAT, '[%Y-%m-%d] [%H:%M:%S]'
))
LOGGER.addHandler(__stream_handler)
LOGGER.setLevel(logging.DEBUG)


def add_file_handler(log_dir: str='./logs', filename: str=_FILE_FORMAT):

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    __file_handler = logging.FileHandler(os.path.join(log_dir, filename))
    __file_handler.setFormatter(logging.Formatter(
        _MSG_FORMAT, '[%Y-%m-%d] [%H:%M:%S]'
    ))
    LOGGER.addHandler(__file_handler)
