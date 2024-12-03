import pika
from faker import Faker
from models import Contact
import json
import connect


def create_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email()
        )
        contact.save()
        contacts.append(str(contact.id))
    return contacts


def send_to_queue(contact_ids):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    for contact_id in contact_ids:
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=json.dumps({'contact_id': contact_id})
        )
        print(f"Sent to queue: {contact_id}")

    connection.close()


if __name__ == "__main__":
    num_contacts = 10 
    contact_ids = create_contacts(num_contacts)
    send_to_queue(contact_ids)
