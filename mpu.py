from mpu6050 import mpu6050
from time import sleep
import smbus

import pika
import time
import sys


"""
sensor=mpu6050(0x68)
print("waiting for the sensor to callibrate")
sleep(2)
while True:
    move='S'
    accel_data=sensor.get_accel_data()
    gyro_data=sensor.get_gyro_data()
    temp=sensor.get_temp()
    x=accel_data['x']
    y=accel_data['y']
    z=accel_data['z']
    print("Accelerometer data")
    print("x:"+str(accel_data['x']))
    print("y:"+str(accel_data['y']))
    print("z:"+str(accel_data['z']))
    if y<-8:
        move='L'
    elif y>8:
        move='R'   
    if x>8:
        move='F'
    elif x<-8:
        move='B'
    if z>8 or z<-8:
        move='S'
        
    print(move)
    
    sleep(1)

"""

RMQ_IP = "localhost"
USERNAME = 'user'
PASSWORD = 'password'
VHOST = 'group6'
ROVER_QUEUE = 'rover_queue'
DATA_QUEUE = 'data_queue'
EXCHANGE = 'exchange'


if __name__== '__main__':		
    sensor=mpu6050(0x68)
    print("waiting for the sensor to callibrate")
    sleep(2)
    
    try:
        credentials = pika.PlainCredentials(username=USERNAME,password=PASSWORD)
        parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=VHOST,credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        print("[Checkpoint] Connected to vhost", VHOST, "on RMQ server at", RMQ_IP, "as user ", USERNAME)

		
        
    except:
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct")
        print("[ERROR] Connection closing")

        if connection:
            connection.close()
        exit(1)	
	
    while True:
        move='S'
        accel_data=sensor.get_accel_data()
        #gyro_data=sensor.get_gyro_data()
        temp=sensor.get_temp()
        x=accel_data['x']
        y=accel_data['y']
        z=accel_data['z']
        print("Accelerometer data")
        print("x:"+str(accel_data['x']))
        print("y:"+str(accel_data['y']))
        print("z:"+str(accel_data['z']))
        if y<-8:
            move='L'
        elif y>8:
            move='R'   
        if x>8:
            move='F'
        elif x<-8:
            move='B'
        if z>8 or z<-8:
            move='S'
        
        print(move)
    
        sleep(1)
	
	    #channel.basic_publish(exchange=rmq_params.get("exchange"),routing_key=rmq_params.get("led_queue"),body=move)
        channel.basic_publish(exchange=EXCHANGE,
                      routing_key=DATA_QUEUE,
                      body=move)

	
	
	
