from datetime import datetime
import pika
import sys
import time
import json

from hw08.database.connect import connect_db
from hw08.database.models import Contacts

def email_task(message):
    # print(f"email_task: {message=}")
    id = message.get("contact_id")
    if id:
        contact = Contacts.objects(id=id).first()
        if contact:
            if not contact.done:
                print(f"Name: {contact.fullname} ")
                print(f"Sending email to: {contact.email}")
                time.sleep(1)
                contact.update(done=True, when_done=datetime.now())
            else:
                print("Task already done")

    return


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)


    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received id: {message.get('id')}")
        email_task(message)

        ch.basic_ack(delivery_tag=method.delivery_tag)


    if connect_db():

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    else:
        print("Database not connected")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)