#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isplogger/isplogger.py
# v.0.2.1
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Houses ISPLogger object, querying specified server for internet access
#

# stdlib imports
from csv import DictWriter
import time
import socket
import datetime
import os

# ISPLogger imports
from isplogger.logger import LOGGER


class ISPLogger:

    def __init__(self, csv_filename: str=None):
        '''ISPLogger: pings a specified server to determine if internet is
        currently available

        Args:
            csv_filename (str): if not None, saves network information to this
                CSV file
        '''

        if csv_filename is not None:
            if not os.path.exists(csv_filename):
                with open(csv_filename, 'w') as csv_file:
                    writer = DictWriter(csv_file, [
                        'Date', 'Time', 'Host', 'Port', 'Status'
                    ], delimiter=',', lineterminator='\n')
                    writer.writeheader()
                csv_file.close()
            self._to_csv = True
            self._csv_filename = csv_filename
        else:
            self._to_csv = False
        return

    def run(self, snapshot_interval: int=10, iterations: int=-1,
            host: str='8.8.8.8', port: int=53, timeout: int=3):
        '''run: main loop to determine if internet access is available; can
        run in endless mode, or for a specified number of iterations

        Args:
            snapshot_interval (int): network is checked every THIS seconds;
                defaults to `10` seconds
            iterations (int): if > 0, runs for THIS number of checks separated
                by snapshot_interval; defaults to `-1`
            host (str): host to ping; defaults to `8.8.8.8`
            port (int): port to ping host on; defaults to `53`
            timeout (int): timeout for the ping; defaults to `3` seconds
        '''

        if timeout > snapshot_interval:
            raise ValueError('Timeout must be < interval: {}, {}'.format(
                timeout, interval
            ))
        if iterations > 0:
            for _ in range(iterations):
                t_start = time.time()
                self.log(
                    self.ping(host, port, timeout),
                    host,
                    port
                )
                t_end = time.time()
                time.sleep(snapshot_interval - (t_end - t_start))
        else:
            while True:
                t_start = time.time()
                self.log(
                    self.ping(host, port, timeout),
                    host,
                    port
                )
                t_end = time.time()
                time.sleep(snapshot_interval - (t_end - t_start))
        return

    def log(self, is_up: bool, host: str, port: int):
        '''log: handles console/file logging, CSV saving

        Args:
            is_up (bool): True if internet is accessable, False otherwise
            host (str): host of attempted connection
            port (int): port of attempted connection
        '''

        if not is_up:
            LOGGER.log(30, 'DOWN',
                       extra={'host_port': '{}:{}'.format(host, port)})
        else:
            LOGGER.log(20, 'UP',
                       extra={'host_port': '{}:{}'.format(host, port)})
        if self._to_csv:
            time_data = self._timestamp()
            status = 1 if is_up else 0
            with open(self._csv_filename, 'a') as csv_file:
                writer = DictWriter(csv_file, [
                    'Date', 'Time', 'Host', 'Port', 'Status'
                ], delimiter=',', lineterminator='\n')
                writer.writerow({
                    'Date': time_data[0],
                    'Time': time_data[1],
                    'Host': host,
                    'Port': port,
                    'Status': status
                })
        return

    @staticmethod
    def ping(host: str, port: int, timeout: int) -> bool:
        '''ping: queries specified address

        Args:
            host (str): host to query
            port (int): port to query host on
            timeout (int): timeout time for query

        Returns:
            bool: True if connection made, False otherwise
        '''

        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (host, port)
            )
            return True
        except Exception as e:
            LOGGER.log(10, 'Exception: {}'.format(e),
                       extra={'host_port': '{}:{}'.format(host, port)})
            return False

    @staticmethod
    def _timestamp() -> tuple:
        '''Obtains the current time

        Returns:
            tuple: (year, month, day, hour, minute, second)
        '''

        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        return (date, time)
