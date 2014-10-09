import logging
import sys
import time
from datetime import datetime, timedelta

import tornado
from tornado.options import options, define
import redis

import dauconfig
import db_config
import dwarf
from dwarf.aubitmap import Bitmap
import dwarf.dau
import dwarf.daux


def get_redis_client(pipe=False):
    conf = db_config.redis_conf
    try:
        if pipe:
            conn = redisPipeline(conf)
        else:
            conn = redis.Redis(**conf)
        return conn
    except Exception, e:
        print "redis connection Error!", e
        raise e

REDIS = get_redis_client()

def _reverse(bmp):
    n = 0
    for b in bmp:
        if b:
            yield n
        n += 1

def _count2id(n, section):
    return section*dauconfig.BITMAP_BLK_LEN+n

def _get_active_bmp(date, section):
    return _get_bitmap(date, 'dau', section)

def _get_newuser_bmp(date, section):
    return _get_bitmap(date, 'dnu', section)

def _lossu_bmp(bmp1, bmp2):
    return bmp1.anti(bmp2)

def _get_bitmap(date, typename, section):
    bmp = Bitmap()
    key_fmt = dauconfig.dau_keys_conf[typename]
    key = key_fmt.format(date=date, month=date)
    if section:
        key = dauconfig.BITMAP_BLK_PREFIX.format(key) % section
    bits = REDIS.get(key)
    return bmp.frombytes(bits)

def get_loss_uid(bdate, tdate):
    ifover = config.MAX_BITMAP_LENGTH % config.BITMAP_BLK_LEN and 1 or 0
    sections = range(dauconfig.MAX_BITMAP_LENGTH/dauconfig.BITMAP_BLK_LEN + plus)
    for sections in sections:
        nbmp = _get_newuser_bmp(bdate, section)
        abmp = _get_active_bmp(tdate, section)
        lbmp = _lossu_bmp(nbmp, abmp)
        for index in _reverse(lbmp):
            uid = _count2id(index, section)
            yield uid

def run():
    define('day')
    define('tday')
    tornado.options.parse_command_line()
    for uid in get_loss_uid(options.day, options.tday):
        sys.stdout.write(uid)
        sys.stdout.write("/n")

if __name__ == '__main__':
    run()

