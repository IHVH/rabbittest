import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.111', credentials= pika.PlainCredentials('test', 'test') ))
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

channel.basic_publish(exchange='syslog',
                      routing_key='qwer',
                      body='log Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()