from datetime import datetime
import pika
from tqdm import tqdm
import json

from hw08.database.connect import connect_db
from hw08.database.seeds import seed_contacts


def seed(
    seed_on: bool = True,
    max_records: int = 100,
    preffer_type: str = "type_email",
    drop: bool = True,
) -> list[str]:
    result = []
    if connect_db():
        if seed_on:
            result = seed_contacts(max_records=max_records, preffer_type=preffer_type)
    return result


def main(
    seed_on: bool = True,
    max_records: int = 100,
    prefer_type: str = "type_email",
    drop: bool = True,
):
    contacts = seed(
        seed_on=seed_on, max_records=max_records, preffer_type=prefer_type, drop=drop
    )
    if not contacts:
        print("contacts not ready")
        return

    try:
        credentials = pika.PlainCredentials("guest", "guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
        )
    except pika.exceptions.AMQPConnectionError:
        print("ERROR RabbitMQ connection")
        return
    
    channel = connection.channel()

    exchange = "task_mock"
    routing_key = "_".join(['task_queue', prefer_type])

    channel.exchange_declare(exchange=exchange, exchange_type="direct")
    channel.queue_declare(queue=routing_key, durable=True)
    channel.queue_bind(exchange=exchange, queue=routing_key)

    for _ in range(2):
        print(f"Sending '{len(contacts)}' contacts ...")
        for i, contact in tqdm(enumerate(contacts, 1), total=len(contacts)):
            message = {
                "id": i,
                "contact_id": contact,
                "date": datetime.now().isoformat(),
                "prefer": prefer_type
            }

            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
            # print(f" [x] {contact}")

    connection.close()


if __name__ == "__main__":
    main(max_records=100,prefer_type="")
