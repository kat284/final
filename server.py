# ~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 2 Python Script
# File name:                Server File (server.py)
# Description:              Script containing the setup and running of the server
# Inputs/Resources:
# Output/Created files:     Server Side Responses
# Written by:               Team 6
# Created:                  04/02/2018
# Last modified:            04/03/2018
# Version:                  1.0.0
# Example usage:            python3 server.py
# Notes:                    N/A
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3

from rmq_params import *
from menu import *
import bluetooth
from bluetooth import *
import pika

# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

RMQ_IP = "localhost"
RFCOMM_CHANNEL = 3
ORDER_ID = 0

# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    try:
        connection = 0
        credentials = pika.PlainCredentials(username=rmq_params.get("username"), password=rmq_params.get("password"))
        parameters = pika.ConnectionParameters(host=RMQ_IP, virtual_host=rmq_params.get("vhost"),
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except:
        print(
            "[ERROR] Unable to connect to vhost: {0} on RMQ server at {1} as user: {2}".format(rmq_params.get("vhost"),
                                                                                               RMQ_IP, rmq_params.get(
                    "username")))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        exit(1)
    print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(rmq_params.get("vhost"),
                                                                                              RMQ_IP, rmq_params.get(
            "username")))
    print("[Checkpoint] Setting up exchanges and queues...")
    channel.exchange_declare(rmq_params.get("exchange"), exchange_type='direct')
    channel.queue_declare(rmq_params.get("order_queue"), auto_delete=True)
    channel.queue_declare(rmq_params.get("led_queue"), auto_delete=True)
    channel.queue_bind(exchange=rmq_params.get("exchange"), queue=rmq_params.get("order_queue"),
                       routing_key=rmq_params.get("order_queue"))
    channel.queue_bind(exchange=rmq_params.get("exchange"), queue=rmq_params.get("led_queue"),
                       routing_key=rmq_params.get("led_queue"))
    try:
        server_socket = 0
        server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_socket.bind((RMQ_IP, RFCOMM_CHANNEL))
        server_socket.listen(1)
    except:
        print("[ERROR] Unable to open the socket")
        print("[ERROR] Bluetooth socket CLOSING")
        if server_socket:
            server_socket.close()
        connection.close()
        exit(1)
    print("[Checkpoint] Bluetooth ready!")
    while 1:
        try:
            print("[Checkpoint] Waiting for connection on RFCOMM channel {0}".format(RFCOMM_CHANNEL))
            client_socket = 0
            client_socket, address = server_socket.accept()
            print("[Checkpoint] Accepted connection from {0}".format(address))
            channel.basic_publish(exchange=rmq_params.get("exchange"), routing_key=rmq_params.get("led_queue"),
                                  body="blue")
            client_socket.send(str(menu))
            print("[Checkpoint] Sent menu:")  # {0}".format(menu))
            for item in menu:
                print("{0}:".format(item))
                for stat in menu[item]:
                    print("    {0}: {1}".format(stat, menu[item][stat]))
            print("")
            order = eval(str(client_socket.recv(1024), 'utf-8'))
            print("[Checkpoint] Received order:")
            print(order)
            ORDER_ID = ORDER_ID + 1
            total_price = 0
            total_time = 0
            for item in order:
                info = menu.get(item)
                if info == None:
                    print("[ERROR] Order has unknown item.")
                    client_socket.close()
                    server_socket.close()
                    connection.close()
                    exit(1)
                total_price = total_price + info.get("price")
                total_time = total_time + info.get("time")
            receipt = {"Order ID": ORDER_ID, "Items": order, "Total Price": total_price, "Total Time": total_time}
            str_receipt = str(receipt)
            client_socket.send(str_receipt)
            print("[Checkpoint] Sent receipt:")  # {0}".format(str_receipt))
            print("    Order ID: {0}".format(ORDER_ID))
            print("    Items: {0}".format(order))
            print("    Total Price: {0}".format(total_price))
            print("    Total Time: {0}".format(total_time))
            channel.queue_declare(str(ORDER_ID), auto_delete=True)
            channel.queue_bind(exchange=rmq_params.get("exchange"), queue=str(ORDER_ID), routing_key=str(ORDER_ID))
            channel.basic_publish(exchange=rmq_params.get("exchange"), routing_key=rmq_params.get("order_queue"),
                                  body=str_receipt)
            submit_msg = "Order Update: Your order has been submitted"
            channel.basic_publish(exchange=rmq_params.get("exchange"), routing_key=str(ORDER_ID), body=submit_msg)
            client_socket.close()
            channel.basic_publish(exchange=rmq_params.get("exchange"), routing_key=rmq_params.get("led_queue"),
                                  body="red")
            print("[Checkpoint] Closed Bluetooth Conection.")
        except:
            print("[ERROR] Communication with the Client Lost or the server.py process was killed")
            print("[ERROR] Bluetooth socket CLOSING")
            if client_socket:
                client_socket.close()
            server_socket.close()
            connection.close()
            exit(1)

# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
