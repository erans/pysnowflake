pysnowflake
===========

pysnowflake is a Python implementation of Twitter's snowflake service - https://github.com/twitter/snowflake

I implemented it in pure Python using the same thrift interfaces because I really dislike the whole overhead the Java Runtime brings with it.
Not to mention the fact that its really hard to run it on small servers with little RAM because you have to fine tune it to the right memory amounts.

With Python its easier and quicker to setup.

Due to various reasons this implementation does not reach the performance indicated in the original Snowflake implementation, however it is good enough
in most cases and can be combined with the help of a software load balancer such as HAProxy to run multiple processes to get higher performance.

You can checkout a Python client implementation I did which I use with this server at: https://github.com/erans/pysnowflakeclient

Installation
------------

* Make sure you have the Thrift Python libraries (0.61 and above would be great)
* Run the service

Usage
-----
usage: pysnowflake.py [-h] [--host HOST] [--port PORT] [--log_level LOG_LEVEL]
                      [--verbose]
                      worker_id data_center_id

Python based Snowflake server

positional arguments:
  worker_id             Worker ID
  data_center_id        Data Center ID

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Host address (default 127.0.0.1)
  --port PORT           port (default 30303)
  --log_level LOG_LEVEL
                        Log level (default: INFO). Values:
                        ERROR,WARN,INFO,DEBUG
  --verbose             Be verbose!


Running it
----------
./pysnowflake worker_id data_center_id (i.e. ./pysnowflake 1 1)


Requirements
------------
* [thirft](http://thrift.apache.org)

Issues
------

Please report any issues via [github issues](https://github.com/erans/pysnowflake/issues)
