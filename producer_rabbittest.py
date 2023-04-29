import pika
count = 9999
msg = 'Hello World!'

host_name = '192.168.1.111'
cred = pika.PlainCredentials('test', 'test')
parametrs = pika.ConnectionParameters(host_name, credentials=cred )

connection = pika.BlockingConnection(parametrs)
channel = connection.channel()
args = {"x-max-length": 1000}
channel.queue_declare(queue='test1000', arguments=args)
channel.queue_declare(queue='hello')
channel.queue_declare(queue='testExclusive', exclusive=True, arguments=args)
channel.queue_declare(queue='testAutoDelete', auto_delete=True, arguments=args)

channel.basic_publish(exchange='', routing_key='testExclusive', body=f'testExclusive {msg} - {count}')
print(f" [x] Sent 'testExclusive {msg} {count}'")

while count > 0:
    channel.basic_publish(exchange='', routing_key='hello', body=f'{msg} - {count}')
    print(f" [x] Sent '{msg} {count}'")
    channel.basic_publish(exchange='', routing_key='test1000', body=f'test1000 {msg} - {count}')
    print(f" [x] Sent 'test1000 {msg} {count}'")
    channel.basic_publish(exchange='syslog', routing_key='rout1', body=f'hello2 {msg} - {count}')
    print(f" [x] Sent 'hello2 {msg} {count}'")
    channel.basic_publish(exchange='', routing_key='testAutoDelete', body=f'testAutoDelete {msg} - {count}')
    print(f" [x] Sent 'testAutoDelete {msg} {count}'")
    count = count - 1

fin = "finished"
channel.basic_publish(exchange='', routing_key='hello', body=fin)
print(f" [x] Sent '{fin}'")

channel.basic_publish(exchange='syslog', routing_key='rout1', body='hello2 ' + fin)
print(f" [x] Sent 'hello2 {fin}'")

connection.close()