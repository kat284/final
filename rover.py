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
from rmq_params import *

# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

RMQ_IP = "localhost"
GPIO_MODE = 10
ROTATION_DIRECTION_PIN = 0
ROTATION_PIN = 0
MOVEMENT_PIN = 0
MOVEMENT_DIRECTION_PIN = 0


# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def callback(ch, method, properties, body):
    body = str(body, 'utf-8')
    if body == "L":
        print("Robot is turning Left")
    elif body == "R":
        print("Robot is turning Right")
    elif body == "F":
        print("Robot is turning Forward")
    elif body == "B":
        print("Robot is turning Backward")
    elif body == "S":
        print("Robot is turning Stop")
    print("[Checkpoint] Current Task is {0}".format(body))


# ~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    if GPIO_MODE == "10":
        GPIO.setmode(GPIO.BOARD)
    else:
        GPIO.setmode(GPIO.BCM)
    #GPIO.setup(RED_PIN, GPIO.OUT)

    try:
        connection = 0
        credentials = pika.PlainCredentials(username=rmq_params.get("username"), password=rmq_params.get("password"))
        parameters = pika.ConnectionParameters(host=RMQ_IP, virtual_host=rmq_params.get("vhost"),
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except:
        print("[ERROR] Unable to connect to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(
            rmq_params.get("vhost"), RMQ_IP, rmq_params.get("username")))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        GPIO.cleanup()
        exit(1)
    print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(rmq_params.get("vhost"),
                                                                                              RMQ_IP, rmq_params.get(
            "username")))
    try:
        channel.queue_bind(exchange=rmq_params.get("exchange"), queue=rmq_params.get("rover_queue"),
                           routing_key=rmq_params.get("rover_queue"))
        channel.basic_consume(callback, queue=rmq_params.get("rover_queue"), no_ack=True)
        print("[Checkpoint] Consuming from RMQ queue: {0}".format(rmq_params.get("rover_queue")))
        channel.start_consuming()
    except:
        print("[ERROR] The queue ({0}) was not found or the rover.py process was killed".format(
            rmq_params.get("rover_queue")))
        print("[ERROR] Verify that the queue is up! You may have to restart the server")
        print("[ERROR] Connection closing")
        connection.close()
        GPIO.cleanup()
        exit(1)

    # ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
