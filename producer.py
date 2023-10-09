import pika
import time
import docker
from faker import Faker
from models import Contact
from connection import connect

num_fake_contacts = 10

client = docker.from_env()
time.sleep(2)
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

# subprocess.Popen("rabbitmq-server", shell=True)

def create_fake_contacts(num_contacts):
    fake = Faker()
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email()
        )
        contact.save()


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')


create_fake_contacts(num_fake_contacts)

for contact in Contact.objects(message_sent=False):
    channel.basic_publish(
        exchange='',
        routing_key='contact_queue',
        body=str(contact.id)
    )
    contact.message_sent = False
    contact.save()

connection.close()
