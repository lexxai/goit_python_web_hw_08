from datetime import datetime
import pika
from tqdm import tqdm
import json

from hw08.database.connect import connect_db
from hw08.database.seeds import seed_contacts


def seed(seed_on: bool = True, max_records: int = 100) -> list[str]:
    result = []
    if connect_db():
        if seed_on:
            result = seed_contacts(max_records=max_records)
    return result


def main(seed_on: bool = True, max_records: int = 100):
    contacts = seed(seed_on=seed_on, max_records=max_records)
    if not contacts:
        print("contacts not ready")
        return

    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    exchange = "task_mock"
    routing_key = "task_queue"

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
    main()
