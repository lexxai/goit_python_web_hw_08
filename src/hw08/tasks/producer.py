import pika


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    
    channel.queue_declare(queue='hello_world')
    text = "Hello world! 1"
    channel.basic_publish(exchange='', routing_key='hello_world', body=text.encode())
    print(f" [x] {text}")
    text = "Hello world! 2"
    channel.basic_publish(exchange='', routing_key='hello_world', body=text.encode())
    print(f" [x] {text}")
    connection.close()
    

if __name__ == '__main__':
    main()