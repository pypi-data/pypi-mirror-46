# ISPLogger: A tool for monitoring/recording internet access

[![GitHub version](https://badge.fury.io/gh/tjkessler%2Fisplogger.svg)](https://badge.fury.io/gh/tjkessler%2Fisplogger)
[![PyPI version](https://badge.fury.io/py/isplogger.svg)](https://badge.fury.io/py/isplogger)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/TJKessler/isplogger/master/LICENSE.txt)

ISPLogger is an open source Python tool for monitoring/logging the availability of an internet connection for a given device. ISPLogger supports text/CSV logging, variable time windows for host pinging and timeouts, and command line/terminal executable functionality.

Future plans for ISPLogger include:
 - Graph generation to display downtime
 - A full graphical user interface

# Installation

Requires Python 3.6+.

Installation via pip:

```
$ pip install isplogger
```

Installation via cloned repository:

```
$ git clone https://github.com/tjkessler/isplogger
$ cd isplogger
$ python setup.py install
```

There are currently no additional dependencies for ISPLogger.

# Usage

## Command line/terminal usage

The easiest way to run ISPLogger is via the command line/terminal:

```
$ isp-logger
```

By default, ISPLogger will ping "8.8.8.8", Google's public DNS servers, every 10 seconds with a 3 second timeout. Unless explicitly stated, no file logging (text or CSV) will occur; instead, network status will be printed to the command line/terminal:

```
[2019-05-19] [15:38:51] [8.8.8.8:53] [INFO] UP
[2019-05-19] [15:39:01] [8.8.8.8:53] [INFO] UP
[2019-05-19] [15:39:11] [8.8.8.8:53] [INFO] UP
[2019-05-19] [15:39:21] [8.8.8.8:53] [INFO] UP
[2019-05-19] [15:39:31] [8.8.8.8:53] [WARNING] DOWN
[2019-05-19] [15:39:41] [8.8.8.8:53] [WARNING] DOWN
```

### Text logging

To save this information to a .log file whose name is the date/time the process was started, specify a directory to put the file with the "log_dir" flag:

```
$ isp-logger --log_dir /path/to/my/logs
```

To change the name of the log file, supply the "log_filename" flag:

```
$ isp-logger --log_dir /path/to/my/logs --log_filename my_network.log
```

ISPLogger logs information at the "debug", "info" and "warning" levels (10, 20 and 30 respectively). "Debug" information includes the exception thrown if a connection could not be made, "info" information includes stating whenever a connection could be made, and "warning" information includes stating whenever a connection could not be made. To change the minimum log level for messages, supply the "log_level" flag and an integer level:

Run ISPLogger at "debug" log level:

```
$ isp-logger --log_level 10
```

Run ISPLogger at "info" log level (default):

```
$ isp-logger --log_level 20
```

Run ISPLogger at "warning" log level:

```
$ isp-logger --log_level 30
```

### CSV file logging

ISPLogger offers the ability to save network status to a CSV file, containing headers for date, time,host/port you are connecting to, and status (1 if a connection was made, 0 otherwise). To save information to a CSV file, supply the "csv_filename" flag and a path to where the file will be created/located:

```
$ isp-logger --csv_filename /path/to/my/network_log.csv
```

### Adjusting timing

ISPLogger will run indefinitely by default. To run ISPLogger for a specified number of iterations, supply the "iterations" flag:

```
$ isp-logger --iterations 50
```

To change the time between network pings, supply the "snapshot_interval" flag and a time in seconds:

```
$ isp-logger --snapshot_interval 30
```

ISPLogger's default timeout is 3 seconds. To change the timeout time, supply the "timeout" flag and a time in seconds:

```
$ isp-logger --timeout 5
```

### Changing host/port

ISPLogger's default connection is "8.8.8.8" on port "53". To change the host ISPLogger connects to, supply the "host" flag:

```
$ isp-logger --host 123.456.78.90
```

Change the port used to connect with the "port" flag:

```
$ isp-logger --host 123.456.78.90 --port 123
```

## Usage within a Python script

ISPLogger can also be used in a Python script. To get started, import the ISPLogger object and initialize it:

```python
from isplogger import ISPLogger

ispl = ISPLogger()
```

To run ISPLogger with default settings (run indefinitely, ping 8.8.8.8 on port 53 every 10 seconds with a 3 second timeout):

```python
from isplogger import ISPLogger

ispl = ISPLogger()
ispl.run()
```

If CSV file logging is desired, specify a path when the ISPLogger is initialized:

```python
ispl = ISPLogger('/path/to/my/network_log.csv')
```

To run ISPLogger for a specified number of iterations:

```python
from isplogger import ISPLogger

ispl = ISPLogger()
ispl.run(iterations=10)
```

To change the time between pings, in seconds:

```python
from isplogger import ISPLogger

ispl = ISPLogger()
ispl.run(snapshot_interval=30)
```

To change the timeout time, in seconds:

```python
from isplogger import ISPLogger

ispl = ISPLogger()
ispl.run(timeout=5)
```

To change the host and/or the port:

```python
from isplogger import ISPLogger

ispl = ISPLogger()
ispl.run(host='123.456.78.90', port='123')
```

Any number of these arguments can be supplied to change ISPLogger's behavior.

To adjust console/text file logging settings, import the LOGGER object:

```python
from isplogger import LOGGER
```

To set the minimum log level:

```python
from isplogger.logger import LOGGER

# Set console/file logging to `debug`
LOGGER.setLevel(10)

# Set console/file logging to `info` (default)
LOGGER.setLevel(20)

# Set console/file logging to `warning`
LOGGER.setLevel(30)
```

To save these log messages to a file named after the current date/time, import the "add_file_handler" function and supply a directory to place the log:

```python
from isplogger import LOGGER, add_file_handler

add_file_handler(LOGGER, log_dir='/path/to/my/logs')
```

To change the name of the log file:

```python
from isplogger import LOGGER, add_file_handler

add_file_handler(LOGGER, log_dir='/path/to/my/logs', filename='my_network.log')
```

To perform a single ping of a specified host/port:

```python
from isplogger import ISPLogger

ispl = ISPLogger()

# Ping 8.8.8.8 on port 53 with a 3 second timeout
result = ispl.ping('8.8.8.8', 53, 3)

# result will be True if connection is made, False if no connection was made
print(result)
```

Logs can be created manually:

```python
from isplogger import ISPLogger

ispl = ISPLogger()

result = ispl.ping('8.8.8.8', 53, 3)

# Pass the `_log` method a boolean value, host and port you are connecting to
ispl.log(result, '8.8.8.8', 53)
```

# Contributing, Reporting Issues and Other Support:

To contribute to ISPLogger, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, inlude information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (travis.j.kessler@gmail.com).
