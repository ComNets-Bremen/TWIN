#!/usr/bin/python

# TWIN node - A Flexible Testbed for Wireless Sensor Networks
# Copyright (C) 2016, Communication Networks, University of Bremen, Germany
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>
#
# This file is part of TWIN

"""HTTP Server for GPIO Pin Access
   Status, Routes on TWIN

   NOTE: For this one needs "Flask Microframework"
        on the Pis.

            sudo pip install flask

        Flask will run on python2 not python3
"""

from flask import Flask, jsonify, request
import json
import RPi.GPIO as gpio


app = Flask(__name__)

GPIO_PINS = [20, 21]  # Using Pins 20, 21 according to BCM layout

HIGH_VALUES = [1, '1', 'HIGH']  # No matter string or integer High is 1

LOW_VALUES = [0, '0', 'LOW']  # No matter string or integer Low is 0

gpio.setmode(gpio.BCM)  # set the BCM layout for the GPIOs

# Set the dedicated GPIO Pins to output mode

for pin in GPIO_PINS:
    gpio.setup(pin, gpio.OUT)


def ioStatus(pinNumber):
    """  Check the GPIO pin's status and return a dictionary

    function: ioStatus

    params: the GPIO pin number (here, 20 or 21)

    Description:
            This function checks if the pin is either 20 or 21.
            If it is either one, return a dictionary
            with the pin number and it's current value
    """
    if pin in GPIO_PINS:
        pinValue = gpio.input(pinNumber)

        # a dictionary of current Pin Status
        statusData = {"pin": pinNumber, "value": pinValue}

    else:
        # if the pin is not 20 nor 21
        statusData = {"status": 'ERROR', "error": 'Invalid Pin Number'}

    # finally return the status

    return statusData


def pinChange(pinNumber, value):
    """  Changes the value of the GPIO pin and returns a dictionary

    function: pinChange

    params: GPIO Pin Number, value to be updated (1 or 0)

    Description:
            This function changes the GPIO Pins value to either High
            or Low. It takes the GPIO pin number and the value and
            sets them and returns a dictionary of the updated value
            of the GPIO Pin
    """

    if pin in GPIO_PINS:
        gpio.output(pinNumber, value)
        updatedValue = gpio.input(pinNumber)  # Update the value of the Pin

        updatedData = {"pin": pinNumber, "newValue": updatedValue}
        pass

    else:
        updatedData = {"status": 'ERROR', "error": 'Invalid pin/value'}

    # finally return the dictionary

    return updatedData


"""Flask APIs """


@app.route('/routes')
@app.route('/routes/')
def routes():
    """  API to retreive the 'routeTable.json' file

    Description:
            This API uses GET resource to return a JSON rendered
            Route Cache that is available on each Pi.

    USAGE:
            curl -g6 http://[fe80::IPV6:LL:ADDR%wlan0]:8080/routes/
                            OR
            curl -g6 http://[fe80::IPV6:LL:ADDR%wlan0]:8080/routes
    """

    with open('/home/pi/routeTable.json') as rFile:
        # Open the file and load it's content
        d = json.load(rFile)

    # Return a JSON Rendered Route Cache upon GET
    return jsonify(d)


@app.route('/gpio/status', methods=['GET'])
@app.route('/gpio/status/', methods=['GET'])
def pin_status():
    """  API to retreive the complete GPIO Pin Configuration

    Description:
            This API uses GET resource to return a JSON rendered
            Status of both the GPIOs on each Pi.

    USAGE:
            curl -g6 http://[fe80::IPV6:LL:ADDR%wlan0]:8080/gpio/status/
                            OR
            curl -g6 http://[fe80::IPV6:LL:ADDR%wlan0]:8080/gpio/status
    """

    listComplete = []  # a complete list of both the GPIOs

    # add status for both the PINS in the list
    for pin in GPIO_PINS:
        listComplete.append(ioStatus(pin))

    status = {'pinStatus': listComplete}

    # Return a JSON Rendered status of GPIOs
    return jsonify(status)


@app.route('/gpio/<pinNumber>', methods=['GET', 'POST'])
@app.route('/gpio/<pinNumber>/', methods=['GET', 'POST'])
def gpioPin(pinNumber):
    """  API to change/view individual GPIO value

    param: value

    Description:
            This API use GET/POST resource to retrieve/change the GPIO
            Pin values. Parameter 'value' is used to set the value.

    USAGE:

    curl -6 --data 'value=1' http://[fe80::IPV6:LL:ADDR%wlan0]:8080/gpio/20/
                        OR

    curl -6 --data 'value=0' http://[fe80::IPV6:LL:ADDR%wlan0]:8080/
            gpio/21/
    """

    pinNumber = int(pinNumber)  # Just to be sure that the input is an int

    if request.method == 'GET':
        pinData = ioStatus(pinNumber)  # return the individual pin config.

    elif request.method == 'POST':
        value = request.values['value']

        if value in HIGH_VALUES:
            pinData = pinChange(pinNumber, 1)
        elif value in LOW_VALUES:
            pinData = pinChange(pinNumber, 0)
        else:
            pinData = {"status": 'ERROR', "error": 'Invalid value'}

    # Finally return JSON rendered Data
    return jsonify(pinData)


if __name__ == '__main__':
    app.run(host='::', port=8080, debug=True)
