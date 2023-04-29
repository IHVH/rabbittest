import pika, sys, os

def main():
    host_name = '192.168.1.111'
    cred = pika.PlainCredentials('test', 'test')
    parametrs = pika.ConnectionParameters(host_name, credentials=cred )

    connection = pika.BlockingConnection(parametrs)
    channel = connection.channel()
    channel2 = connection.channel()
    channel3 = connection.channel()

    args = {"x-max-length": 1000}
    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='test1000', arguments=args)
    channel2.queue_declare(queue='hello2', durable=True)
    #channel3.queue_declare(queue='testExclusive', exclusive=True, arguments=args)
    channel3.queue_declare(queue='testAutoDelete', auto_delete=True, arguments=args)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='test1000', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    channel2.basic_consume(queue='hello2', on_message_callback=callback, auto_ack=True)
    #channel3.basic_consume(queue='testExclusive', on_message_callback=callback, auto_ack=True)
    channel3.basic_consume(queue='testAutoDelete', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    channel2.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)