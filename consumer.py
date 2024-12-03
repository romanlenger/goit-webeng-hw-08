import pika
import json
from models import Contact
import connect

def send_email(contact):
    print(f"Sending email to {contact.fullname} at {contact.email}...")
    return True


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects(id=contact_id).first()

    if contact and not contact.message_sent:
        if send_email(contact):
            contact.message_sent = True
            contact.save()
            print(f"Email sent and status updated for {contact.fullname}.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    print("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    consume()
