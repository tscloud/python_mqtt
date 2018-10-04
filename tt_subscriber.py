#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import sqlite3, ConfigParser
from datetime import datetime, date

#MQTT_SERVER = "bigasspi"
#MQTT_PATH1 = "/test/htu21d"
#MQTT_PATH2 = "/test/bme280"
#DB_LOCATION = "/home/tscloud/mqtt_db/kegstats.db"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH1)
    client.subscribe(MQTT_PATH2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #print('insert_data:')

    try:
        # -- parse out desired data
        # Txx.x,Hyy.y,Pzz.z
        msg_data = (str(msg.payload)).split(",")
        insert_data = [datetime.now()]
        col_list ="(capturetime,"
        value_list = " VALUES(?"
        for x in msg_data:
            if x.startswith('T'):
                insert_data.append(float(x[1:]))
                col_list += "temp,"
                value_list += ",?"
                continue
            if x.startswith('H'):
                insert_data.append(float(x[1:]))
                col_list += "humidity,"
                value_list += ",?"
                continue
            if x.startswith('P'):
                insert_data.append(float(x[1:]))
                col_list += "pressure,"
                value_list += ",?"
                continue
        insert_data.append(msg.topic)
        col_list += "channel)"
        value_list += ",?)"
        #print(insert_data)
        #print(col_list)
        #print("INSERT OR REPLACE INTO kegstatus " + col_list + value_list)

        #sqlite_cur.execute('''INSERT OR REPLACE INTO kegstatus
        #    (capturetime, temp, humidity, pressure, channel)
        #    VALUES(?,?,?,?,?)''', insert_data)
        sqlite_cur.execute("INSERT OR REPLACE INTO kegstatus " + col_list + value_list, insert_data)
        sqlite_conn.commit()

    except Exception as e:
        print e
        print "db prob...exiting on_message()"

try:
    # -- read config file
    config = ConfigParser.RawConfigParser()
    ### I think this is weird -- have to do this to make the options not convert to lowercase
    config.optionxform = str
    config.read("subscriber_config.ini")

    MQTT_SERVER = config.get("MQTT", "MQTT_SERVER")
    MQTT_PATH1 = config.get("MQTT", "MQTT_PATH1")
    MQTT_PATH2 = config.get("MQTT", "MQTT_PATH2")
    DB_LOCATION = config.get("DB", "DB_LOCATION")

    # -- setup DB connection
    sqlite_conn = sqlite3.connect(DB_LOCATION)
    sqlite_cur = sqlite_conn.cursor()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_SERVER, 1883, 60)

	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
    client.loop_forever()

except Exception as e:
    print e
    print "bad stuff...exiting"

finally:
    sqlite_conn.close()
    client.disconnect()
    print "\nBye"
