#!/usr/bin/python

import datetime

from Snowflake import Snowflake
from Snowflake.ttypes import *
from Snowflake.constants import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def timedelta_ms(td):
	return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

transport = TSocket.TSocket('localhost', 30303)
transport = TTransport.TFramedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
 
client = Snowflake.Client(protocol)
 
transport.open()

ids_created = 0
start_time = datetime.datetime.utcnow()

for i in range(0, 1000000):
	client.get_id("test")
	ids_created += 1
	
taken = datetime.datetime.utcnow() - start_time
taken_ms = timedelta_ms(taken)

print "ids created: %i" % ids_created
print "Duration (ms): %s" % (taken_ms) 
print "Duration: %s" % (taken)
print "Avg. Creation Time: %s ms" % (taken_ms / float(ids_created))


