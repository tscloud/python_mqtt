#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import sqlite3

print 'create sqlite DB & table...'

try:
    sqlite_conn = sqlite3.connect('/home/pi/mqtt_db/kegstats.db')
    sqlite_cur = sqlite_conn.cursor()

    sqlite_cur.execute("""
        CREATE TABLE if not exists kegstatus(capturetime INTEGER PRIMARY KEY,
            temp TEXT, humidity TEXT, pressure TEXT, channel TEXT)
        """)
    sqlite_conn.commit()

    print '...success'

except Exception as e:
    print e
    print 'bad opt...exiting'
    sys.exit()

finally:
    sqlite_conn.close()
