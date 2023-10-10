import time
from models_contact import Contact


def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    sended = contact.message_sent
    if contact and not sended:
        print(f"Відправлено листа до {contact.email}")
        time.sleep(2)
        contact.message_sent = True
        contact.save()
