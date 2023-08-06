#!/usr/bin/python
# coding:utf-8

import config
import pymysql
from DBUtils.PooledDB import PooledDB
from contextlib import contextmanager

# 数据库连接池
pool = None


def init():
    if not config.Mysql['active']:
        return

    global pool
    if pool is None:
        config_opt = {
            'host': config.Mysql['host'],
            'port': config.Mysql['port'],
            'user': config.Mysql['user'],
            'password': config.Mysql['pwd'],
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }
        pool = PooledDB(pymysql, **config_opt)


@contextmanager
def create_cursor():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()


