# coding: utf-8

import logging
import sys
import time
import re
from datetime import datetime, timedelta
import redis

import tornado
import tornado.options
from tornado.options import options, define

time_str_fmt_sns = '%Y-%m-%d %H:%M:%S'
time_str_fmt_nginx = '%d/%b/%Y:%H:%M:%S'

snslog_reg_str = r'(?P<dt>\d+-\d\d-\d\d [0-9:]+).*<(?P<event>[a-z]+) from=[\'|"](?P<uid>[0-9]+)[\'|"].*'

rkey_event_nums = 'hEvs{date}'

def get_redis_client(pipe=False):
    conf = db_config.redis_conf
    try:
        if pipe:
            conn = redisPipeline(conf)
        else:
            conn = redis.Redis(host='127.0.0.1', port=6379, db=1)
        return conn
    except Exception, e:
        print "redis connection Error!", e
        raise e

def read_uids(filename):
	uids = []
	with open(filename) as f:
		for line in f:
			try:
				#uid = int(line)			
				uids.append(line.strip())
			except:
				pass
	return uids

def collect_snslog(filename, uids):
	#redisconn = get_redis_client()
	evs = {}
	with open(filename) as logf:
		for line in logf:
			r = re.search(snslog_reg_str,line)
			if r:
				d = r.groupdict()
				if d.get('uid') in uids:
					logging.debug(d)
					ev = d.get('event')
					evs.update({ev:evs.get(ev,0)+1})
	print evs
	for k,v in evs.items():
		print '%s,%s' % (k,v)

def stat_evs(env, redisconn):
	pass

def _str2time(tstr, fmt):
	datetime.strptime()
	return

def run(logf, uidf):
	uids = read_uids(uidf)
	collect_snslog(logf, uids)

def main():
	define('logf', help='日志文件位置')
	define('uidf', help='用户ID文件位置')
	define('date', help='统计日期')
	tornado.options.parse_command_line()
	run(options.logf, options.uidf)

if __name__ == '__main__':
	main()
