#!/usr/bin/python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Written by Eran Sandler (eran@sandler.co.il)
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
	transport = TSocket.TServerSocket(host=args.host, port=args.port)
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