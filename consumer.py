import docker
import pika
import time
from models import Contact, StringField, EmailField, BooleanField
from connection import connect

client = docker.from_env()
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


def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Відправлено листа до {contact.email}")
        time.sleep(2)
        contact.message_sent = True
        contact.save()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')



def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email(contact_id)


channel.basic_consume(queue='contact_queue',
                      on_message_callback=callback, auto_ack=True)

print('Чекаю на повідомлення. Для виходу натисніть Ctrl+C')
channel.start_consuming()
