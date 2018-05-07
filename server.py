from flask import Flask, request, jsonify, make_response, send_file
from rmq_params import *
import pika
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
app = Flask(__name__)
db = client['test_database']


RMQ_IP = "localhost"
USERNAME = 'user'
PASSWORD = 'password'
VHOST = 'group6'
ROVER_QUEUE = 'rover_queue'
DATA_QUEUE = 'data_queue'
EXCHANGE = 'exchange'

def callback(ch, method, properties, body):
    body=str(body,'utf-8')

    rover_direction = body
    
    db.posts.remove({})
    
    data_set1 = {"name": "data", "direction": rover_direction}
    
    print("[Checkpoint] Storing into MongoDB... {0}".format(data_set1))

    if not db.posts.find_one({"w":1}):
        data1 = db.posts.insert_one(data_set1)
        data2 = db.posts.insert_one({"w":1})
    else:
        data1 = db.posts.update({"name": "data"}, { '$set': {"direction": rover_direction}})

    data_new = db.posts.distinct("direction")

    channel.basic_publish(exchange=EXCHANGE,
                      routing_key=ROVER_QUEUE,
                      body=str(data_new.pop()))   
    #channel.basic_publish(exchange=EXCHANGE,
    #                  routing_key=ROVER_QUEUE,
    #                  body=data_new)




if __name__ == '__main__':
    try:
        connection = 0
        credentials = pika.PlainCredentials(username=USERNAME,password=PASSWORD)
        parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=VHOST,credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except:
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        exit(1)
    print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(VHOST,RMQ_IP,USERNAME))
    print("[Checkpoint] Setting up exchanges and queues...")
    channel.exchange_declare(exchange = EXCHANGE, exchange_type = 'direct')
    channel.queue_declare(DATA_QUEUE, auto_delete=True)
    channel.queue_declare(ROVER_QUEUE, auto_delete=True)
    channel.queue_bind(exchange=EXCHANGE,queue=DATA_QUEUE,routing_key=DATA_QUEUE)
    channel.queue_bind(exchange=EXCHANGE,queue=ROVER_QUEUE,routing_key=ROVER_QUEUE)
    while 1:
        try:
            channel.basic_consume(callback, queue=DATA_QUEUE, no_ack=True)
            print("[Checkpoint] Consuming from RMQ queue:", DATA_QUEUE)
            channel.start_consuming()
        except:
            print("[ERROR] Communication with the Client Lost or the server.py process was killed")
            connection.close()
            exit(1)


