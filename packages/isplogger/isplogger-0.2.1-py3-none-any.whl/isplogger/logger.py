#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isplogger/logger.py
# v.0.2.1
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Console/text file logging
#

# stdlib imports
import logging
import datetime
import os


_MSG_FORMAT = '%(asctime)s [%(host_port)s] [%(levelname)s] %(message)s'
FILE_FORMAT = '{}.log'.format(datetime.datetime.now().strftime(
    '%Y%m%d%H%M%S'
))
LOGGER = logging.getLogger('down_detector')
__stream_handler = logging.StreamHandler()
__stream_handler.setFormatter(logging.Formatter(
    _MSG_FORMAT, '[%Y-%m-%d] [%H:%M:%S]'
))
LOGGER.addHandler(__stream_handler)
LOGGER.setLevel(logging.DEBUG)


def add_file_handler(log_object: logging.Logger, log_dir: str='./logs',
                     filename: str=FILE_FORMAT):
    '''add_file_handler: adds file saving to supplied logging.Logger object

    Args:
        log_object (logging.Logger): logger object to add handler to
        log_dir (str): directory to place logs
        filename (str): name of the log file; defaults to date/time-stamp
    '''

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    __file_handler = logging.FileHandler(os.path.join(log_dir, filename))
    __file_handler.setFormatter(logging.Formatter(
        _MSG_FORMAT, '[%Y-%m-%d] [%H:%M:%S]'
    ))
    log_object.addHandler(__file_handler)
    return
