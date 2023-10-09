import time
from models import Contact


def send_sms(contact_id):
    contact = Contact.objects(id=contact_id).first()
    sended = contact.message_sent
    if contact and not sended:
        print(f"Відправлено SMS до {contact.phone_number}")
        time.sleep(2)
        contact.message_sent = True
        contact.save()
