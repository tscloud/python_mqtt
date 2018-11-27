#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import datetime
app = Flask(__name__)

@app.route("/")
def getSensorData():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    temp = 0
    humidity = 0
    pressure = 0

    templateData = {
        'title' : 'SENSOR!',
        'time' : timeString,
        'temp' : temp,
        'humidity': humidity,
        'pressure': pressure
    }

    return render_template('sensor.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8088, debug=True)
