#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isplogger/cmd_line.py
# v.0.2.1
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Command line tool for running isplogger: run as `isp-logger`
#

# stdlib imports
from argparse import ArgumentParser
from sys import argv

# ISPLogger imports
from isplogger import ISPLogger
from isplogger import LOGGER, add_file_handler, FILE_FORMAT


def main():

    ap = ArgumentParser()
    ap.add_argument(
        '--csv_filename',
        type=str,
        default=None,
        help='If saving to CSV, specify the CSV\'s file location'
    )
    ap.add_argument(
        '--snapshot_interval',
        type=int,
        default=10,
        help='Network is tested every X seconds; defaults to 10'
    )
    ap.add_argument(
        '--iterations',
        type=int,
        default=-1,
        help='Tests for X iterations; default is infinite loop (-1)'
    )
    ap.add_argument(
        '--log_level',
        type=int,
        default=20,
        help='Console stream minimum log level; defaults to 20 (INFO)'
    )
    ap.add_argument(
        '--log_dir',
        type=str,
        default=None,
        help='If additional text-file logging is desired, specify a directory '
             'to save them in'
    )
    ap.add_argument(
        '--log_filename',
        type=str,
        default=FILE_FORMAT,
        help='Name of text log file, if saving to file'
    )
    ap.add_argument(
        '--host',
        type=str,
        default='8.8.8.8',
        help='Host to ping to test internet access; defaults to `8.8.8.8`'
    )
    ap.add_argument(
        '--port',
        type=int,
        default=53,
        help='Port to connect to host with; defaults to `53`'
    )
    ap.add_argument(
        '--timeout',
        type=int,
        default=3,
        help='Timeout, in seconds, of network pings; defaults to 3'
    )
    args = vars(ap.parse_args(argv[1:]))
    ispl = ISPLogger(args['csv_filename'])
    LOGGER.setLevel(args['log_level'])
    if args['log_dir'] is not None:
        add_file_handler(LOGGER, log_dir=args['log_dir'],
                         filename=args['log_filename'])
    ispl.run(args['snapshot_interval'], args['iterations'], args['host'],
             args['port'], args['timeout'])
