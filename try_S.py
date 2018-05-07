import sys
import pika

RMQ_IP = "localhost"
USERNAME = 'user'
PASSWORD = 'password'
VHOST = 'group6'
ROVER_QUEUE = 'rover_queue'
DATA_QUEUE = 'data_queue'
EXCHANGE = 'exchange'

if __name__ == '__main__':

   try:
        connection = 0
        credentials = pika.PlainCredentials(username=USERNAME,password=PASSWORD)
        parameters = pika.ConnectionParameters(host=RMQ_IP,virtual_host=VHOST,credentials=credentials)
        connection = pika.BlockingConnection(parameters)      
        
#        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        channel = connection.channel()
   except:
        print("[ERROR] Unable to connect to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(VHOST,RMQ_IP, USERNAME))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        exit(1)
   print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(VHOST,RMQ_IP, USERNAME))
   try:
       channel.basic_publish(exchange=EXCHANGE,
                             routing_key=DATA_QUEUE,
                             body="S")
#       channel.queue_bind(exchange=rmq_params.get("exchange"),queue=rmq_params.get("led_queue"),routing_key=rmq_params.get("led_queue")) 
#       channel.basic_consume(callback,queue=rmq_params.get("led_queue"),no_ack=True) 
#       print("[Checkpoint] Consuming from RMQ queue: {0}".format(rmq_params.get("led_queue"))) 
#       channel.start_consuming() 
   except:
       print("[ERROR] The queue ({0}) was not found or the try.py process was killed".format(DATA_QUEUE))
       print("[ERROR] Verify that the queue is up! You may have to restart the server")
       print("[ERROR] Connection closing")
       connection.close()
       exit(1)    

#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
