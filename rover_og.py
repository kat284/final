# ~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 2 Python Script
# File name:                Led File (led.py)
# Description:              Script containing the setup and running of the led portion of the server
# Inputs/Resources:
# Output/Created files:     Led Responses
# Written by:               Team 6
# Created:                  04/02/2018
# Last modified:            04/03/2018
# Version:                  1.0.0
# Example usage:            python3 led.py -s <RMQ IP OR HOSTNAME>
#                                               -m <GPIO MODE>
#                                               -r <RED PIN NUMBER>
#                                               -g <GREEN PIN NUMBER>
#                                               -b <BLUE PIN NUMBER>
# Notes:                    N/A
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3

import RPi.GPIO as GPIO
import bluetooth
import sys
import pika
import pifacedigitalio
import pifaceio
pfio = pifaceio.PiFace()
pfdio = pifacedigitalio.PiFaceDigital()
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

RMQ_IP = "localhost"
GPIO_MODE = 10
ROTATION_DIRECTION_PIN_1 = 0
ROTATION_DIRECTION_PIN_2 = 0
ROTATION_ENABLE_PIN = 0
MOVEMENT_DIRECTION_PIN_1 = 0
MOVEMENT_DIRECTION_PIN_2 = 0
MOVEMENT_ENABLE_PIN = 0

# --[PIN_LAYOUT]--#
# [5V 0 1 2 3 4 5 6 7][0 1 2 3 4 5 6 7 GND]
PF_ROTATION_ENABLE_PIN = 5
PF_ROTATION_DIRECTION_PIN_1 = 4
PF_ROTATION_DIRECTION_PIN_2 = 3
PF_MOVEMENT_DIRECTION_PIN_1 = 2
PF_MOVEMENT_DIRECTION_PIN_2 = 1
PF_MOVEMENT_ENABLE_PIN = 0

USERNAME = 'user'
PASSWORD = 'password'
VHOST = 'group6'
ROVER_QUEUE = 'rover_queue'
EXCHANGE = 'exchange'
PIFACE_CONNECTED = True

# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def callback(ch, method, properties, body):
    body = str(body, 'utf-8')
    if PIFACE_CONNECTED:
        if body == "F":
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_on()
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_on()
            pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_off()
        elif body == "L":
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_on()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_off()
            pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_on()
        elif body == "R":
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_on()
            pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_off()
            pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_on()
        elif body == "B":
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_on()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_on()
            pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_off()
        elif body == "S":
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_off()
            pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_off()
        else:
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_off()
            pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_off()
            pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_off()
            pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_off()
            print("[ERROR] Unknown Message: {0}".format(body))
            body = "S"
    else:
        if body == "F":
            GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(ROTATION_ENABLE_PIN, GPIO.LOW)
            GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.HIGH)
        elif body == "L":
            GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(ROTATION_ENABLE_PIN, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.LOW)
        elif body == "R":
            GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.LOW)
            GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.HIGH)
            GPIO.output(ROTATION_ENABLE_PIN, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.LOW)
        elif body == "B":
            GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(ROTATION_ENABLE_PIN, GPIO.LOW)
            GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.LOW)
            GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.HIGH)
            GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.HIGH)
        elif body == "S":
            GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(ROTATION_ENABLE_PIN, GPIO.LOW)
            GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.LOW)
        else:
            GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(ROTATION_ENABLE_PIN, GPIO.LOW)
            GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.HIGH)
            GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.LOW)
            GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.LOW)
            print("[ERROR] Unknown Message: {0}".format(body))
            body = "S"""
    print("[Checkpoint] Setting Rover Based on Message: {0}".format(body))

# ~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

    if PIFACE_CONNECTED:
        pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_1].turn_off()
        pfdio.leds[PF_MOVEMENT_DIRECTION_PIN_2].turn_off()
        pfdio.leds[PF_ROTATION_DIRECTION_PIN_1].turn_off()
        pfdio.leds[PF_ROTATION_DIRECTION_PIN_2].turn_off()
        pfdio.leds[PF_MOVEMENT_ENABLE_PIN].turn_off()
        pfdio.leds[PF_ROTATION_ENABLE_PIN].turn_off()
    else:
        if GPIO_MODE == "10":
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(ROTATION_DIRECTION_PIN_1, GPIO.OUT)
        GPIO.setup(ROTATION_DIRECTION_PIN_2, GPIO.OUT)
        GPIO.setup(ROTATION_ENABLE_PIN, GPIO.OUT)
        GPIO.setup(MOVEMENT_DIRECTION_PIN_1, GPIO.OUT)
        GPIO.setup(MOVEMENT_DIRECTION_PIN_2, GPIO.OUT)
        GPIO.setup(MOVEMENT_ENABLE_PIN, GPIO.OUT)

        GPIO.output(ROTATION_DIRECTION_PIN_1, GPIO.HIGH)
        GPIO.output(ROTATION_DIRECTION_PIN_2, GPIO.LOW)
        GPIO.output(ROTATION_ENABLE_PIN, GPIO.LOW)
        GPIO.output(MOVEMENT_DIRECTION_PIN_1, GPIO.HIGH)
        GPIO.output(MOVEMENT_DIRECTION_PIN_2, GPIO.LOW)
        GPIO.output(MOVEMENT_ENABLE_PIN, GPIO.LOW)

    try:
        connection = 0
        credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
        parameters = pika.ConnectionParameters(host=RMQ_IP, virtual_host=VHOST,credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except:
        print("[ERROR] Unable to connect to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(PASSWORD, RMQ_IP, USERNAME))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        if not PIFACE_CONNECTED:
            GPIO.cleanup()
        exit(1)
    print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(VHOST, RMQ_IP, USERNAME))
    try:
        channel.queue_bind(exchange=EXCHANGE, queue=ROVER_QUEUE, routing_key=ROVER_QUEUE)
        channel.basic_consume(callback, queue=ROVER_QUEUE, no_ack=True)
        print("[Checkpoint] Consuming from RMQ queue: {0}".format(ROVER_QUEUE))
        channel.start_consuming()
    except:
        print("[ERROR] The queue ({0}) was not found or the rover.py process was killed".format(ROVER_QUEUE))
        print("[ERROR] Verify that the queue is up! You may have to restart the server")
        print("[ERROR] Connection closing")
        connection.close()
        if not PIFACE_CONNECTED:
            GPIO.cleanup()
        exit(1)

#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
