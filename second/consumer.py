import pika
import time
import docker

from models_contact import Contact
from consumer_email import send_email
from consumer_sms import send_sms
from connection import connect

client = docker.from_env()
time.sleep(4)
existing_containers = client.containers.list(
    all=True, filters={"name": "rabbitmq"})

if not existing_containers:
    client.containers.run(
        "rabbitmq:3.12-management",
        name="rabbitmq",
        detach=True,
        ports={"5672/tcp": 5672, "15672/tcp": 15672},
    )
else:
    print("Контейнер 'rabbitmq' вже запущений.")


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact:
        if contact.best_contact_method == "SMS":
            send_sms(contact_id)
        elif contact.best_contact_method == "Email":
            send_email(contact_id)

        contact.message_sent = True
        contact.save()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# channel.queue_declare(queue='contact_queue')

channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=True)

print('Чекаю на повідомлення. Для виходу натисніть Ctrl+C')
channel.start_consuming()
