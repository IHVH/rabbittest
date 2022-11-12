import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.111', credentials= pika.PlainCredentials('test', 'test') ))
    channel = connection.channel()
    channel2 = connection.channel()

    channel.queue_declare(queue='hello')
    channel2.queue_declare(queue='hello2', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    channel2.basic_consume(queue='hello2', on_message_callback=callback, auto_ack=True)

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