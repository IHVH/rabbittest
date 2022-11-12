import pika
count = 9999
msg = 'Hello World!'
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.111', credentials= pika.PlainCredentials('test', 'test') ))
channel = connection.channel()
channel.queue_declare(queue='hello')

while count > 0:
    channel.basic_publish(exchange='', routing_key='hello', body=f'{msg} - {count}')
    print(f" [x] Sent '{msg} {count}'")
    channel.basic_publish(exchange='syslog', routing_key='qwer', body=f'hello2 {msg} - {count}')
    print(f" [x] Sent 'hello2 {msg} {count}'")
    count = count - 1

fin = "finished"
channel.basic_publish(exchange='', routing_key='hello', body=fin)
print(f" [x] Sent '{fin}'")

channel.basic_publish(exchange='syslog', routing_key='qwer', body='hello2 ' + fin)
print(f" [x] Sent 'hello2 {fin}'")

connection.close()