#!/usr/bin/python
# coding:utf-8

import redis
import config

# Redis客户端对象
rds = None


def init():
    if not config.Redis['active']:
        return

    global rds

    if rds is None:
        rds = redis.Redis(host=config.Redis['host'], port=config.Redis['port'], decode_responses=True)


