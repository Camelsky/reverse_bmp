#!/usr/bin/env python
#coding:utf-8
import logging
import sys
import time

import tornado
from tornado.options import options, define
import redis

import dauconfig
import db_config
import dwarf
from dwarf.aubitmap import Bitmap
import dwarf.dau
import dwarf.daux


def get_redis_client(rediss=1 ,pipe=False):
    if rediss == 1:
        conf = db_config.redis_conf
    else:
        conf = db_config.redis_conf2
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
REDIS2 = get_redis_client(rediss=2)


def get_keys():
    keys = REDIS.keys('*')
    return keys

def read(key):
    Type = REDIS.type(key)
    if Type == 'string':
        return REDIS.get(key)
    elif Type == 'hash':
        return REDIS.hgetall(key)

def save(key, data, Type):
    if Type == 'string':
        REDIS2.set(key, data)
    elif Type == 'hash':
        REDIS2.hmset(key, data)

def trans():
    for key in get_keys():
        Type = REDIS.type(key)
        logging.info('trans %s type:%s', key, Type)
        data = read(key)
        save(key, data, Type)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    trans()

