#!/bin/sh
rm *.deb
fpm -s dir -t deb -n "megamsnowflake" -v 0.5 -d "python,python-thrift" --after-install ./postinst --deb-upstart ./etc/init/snowflake --license "Apache V2" --vendor "Megam Systems" --maintainer "<rajthilak@megam.co.in>" --url "http://www.gomegam.com" --description "Python based unique id generator server based on Twitters snowflake. source : https://github.com/erans/pysnowflake.git" ./usr/share/megam/snowflake/bin
