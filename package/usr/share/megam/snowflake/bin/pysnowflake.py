#!/usr/bin/python
#
# Copyright (c) 2011 Eran Sandler (eran@sandler.co.il),  http://eran.sandler.co.il,  http://forecastcloudy.net
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import argparse
import logging
import socket

from Snowflake import Snowflake
from Snowflake.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TNonblockingServer, TServer

from idworker import IdWorker

DEBUG_LEVELS = {
	"ERROR" : logging.ERROR,
	"WARN"	: logging.WARNING,
	"INFO"  : logging.INFO,
	"DEBUG" : logging.DEBUG
}

def get_log_level(debug_level_string):
	d = debug_level_string.upper()
	if d in DEBUG_LEVELS:
		return DEBUG_LEVELS[d]
	
	return logging.INFO

def run(args):
	log_level = get_log_level(args.log_level)
	
	logger = logging.getLogger()
	logger.setLevel(log_level)
	if args.verbose:
		ch = logging.StreamHandler()
		ch.setLevel(log_level)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		ch.setFormatter(formatter)
		logger.addHandler(ch)

	logging.info("Starting pysnowflake server %s:%d" % (args.host, args.port))
	
	handler = IdWorker(args.worker_id, args.data_center_id)
	processor = Snowflake.Processor(handler)
	transport = TSocket.TServerSocket(port=args.port)
	tfactory = TTransport.TBufferedTransportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()

	logging.info("logging level: %s" % args.log_level)
	server = TNonblockingServer.TNonblockingServer(processor, transport, pfactory, threads=1)
	logging.info("RUNNING")
	server.serve()
	
def main():
	parser = argparse.ArgumentParser(description='Python based Snowflake server')
	parser.add_argument("worker_id", type=int, help="Worker ID")
	parser.add_argument("data_center_id", type=int, help="Data Center ID")
	parser.add_argument("--host", type=str, help="Host address (default 127.0.0.1)", default="127.0.0.1")
	parser.add_argument("--port", type=int, help="port (default 30303)", default=30303)
	parser.add_argument("--log_level", type=str, help="Log level (default: INFO). Values: ERROR,WARN,INFO,DEBUG", default="INFO")
	parser.add_argument("--verbose", help="Be verbose!", action="store_true")
	
	args = parser.parse_args()
	run(args)
	
if __name__ == "__main__":
	main()
