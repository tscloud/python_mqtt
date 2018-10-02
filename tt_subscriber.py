#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import sqlite3

MQTT_SERVER = "localhost"
MQTT_PATH1 = "/test/htu21d"
MQTT_PATH2 = "H1_channel"

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
    # more callbacks, etc
    
    try:
		
	except Exception as e:
		print e
		print 'bad db stuff...exiting'
		sys.exit()

	finally:
		sqlite_conn.close()

try:
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(MQTT_SERVER, 1883, 60)

	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	client.loop_forever()

except KeyboardInterrupt:
	print "User Cancelled (Ctrl C)"

finally:
	client.disconnect()
	print "\nBye"
