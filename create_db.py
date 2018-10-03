#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, date
import sqlite3

print 'create sqlite DB & table...'

try:
    sqlite_conn = sqlite3.connect('/home/tscloud/mqtt_db/kegstats.db',detect_types=sqlite3.PARSE_DECLTYPES)
    sqlite_cur = sqlite_conn.cursor()

    # create table but only if not already exists
    sqlite_cur.execute('''
        CREATE TABLE if not exists kegstatus(capturetime [timestamp] PRIMARY KEY,
            temp REAL, humidity REAL, pressure REAL, channel TEXT)
        ''')
    sqlite_conn.commit()

    print 'creation...success'

    # do test insert
    items = [datetime.now(),69.9,98.1,1080.1,'/channel']
    sqlite_cur.execute('''INSERT OR REPLACE INTO kegstatus
        (capturetime, temp, humidity, pressure, channel)
        VALUES(?,?,?,?,?)''', items)
    sqlite_conn.commit()

    print 'insert...success'

except Exception as e:
    print e
    print 'bad opt...exiting'

finally:
    sqlite_conn.close()
