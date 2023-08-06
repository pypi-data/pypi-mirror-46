#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# isplogger/isplogger.py
# v.0.1.0
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Houses ISPLogger object, querying specified server for internet access
#

from csv import DictWriter
import time
import socket
import datetime
import os

from isplogger.logger import LOGGER


class ISPLogger:

    def __init__(self, to_csv: bool=False,
                 csv_filename: str='./down_time.csv'):
        '''ISPLogger: pings a specified server to determine if internet is
        currently available

        Args:
            to_csv (bool): if True, logs all data to a CSV file; defaults to
                False
            csv_filename (str): if `to_csv` is True, saves to this file;
                defaults to `./down_time.csv`
        '''

        if to_csv:
            if not os.path.exists(csv_filename):
                with open(csv_filename, 'w') as csv_file:
                    writer = DictWriter(csv_file, [
                        'Year', 'Month', 'Day', 'Hour',
                        'Minute', 'Second', 'Status'
                    ], delimiter=',', lineterminator='\n')
                    writer.writeheader()
                csv_file.close()
        self._to_csv = to_csv
        self._csv_filename = csv_filename
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
                self._log(self.ping(host, port, timeout))
                t_end = time.time()
                time.sleep(snapshot_interval - (t_start - t_end))
        else:
            while True:
                t_start = time.time()
                self._log(self.ping(host, port, timeout))
                t_end = time.time()
                time.sleep(snapshot_interval - (t_start - t_end))
        return

    def _log(self, is_up: bool):
        '''_log: handles console/file logging, CSV saving

        Args:
            is_up (bool): True if internet is accessable, False otherwise
        '''

        if not is_up:
            LOGGER.log(30, 'DOWN')
        else:
            LOGGER.log(20, 'UP')
        if self._to_csv:
            time_data = self._timestamp()
            status = 1 if is_up else 0
            with open(self._csv_filename, 'a') as csv_file:
                writer = DictWriter(csv_file, [
                    'Year', 'Month', 'Day', 'Hour',
                    'Minute', 'Second', 'Status'
                ], delimiter=',', lineterminator='\n')
                writer.writerow({
                    'Year': time_data[0],
                    'Month': time_data[1],
                    'Day': time_data[2],
                    'Hour': time_data[3],
                    'Minute': time_data[4],
                    'Second': time_data[5],
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
            LOGGER.log(10, 'Exception: {}'.format(e))
            return False

    @staticmethod
    def _timestamp() -> tuple:
        '''Obtains the current time

        Returns:
            tuple: (year, month, day, hour, minute, second)
        '''

        now = datetime.datetime.now()
        return (now.year, now.month, now.day, now.hour, now.minute, now.second)
