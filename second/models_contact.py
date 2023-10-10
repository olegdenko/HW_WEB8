from mongoengine import Document, StringField, EmailField, BooleanField


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    best_contact_method = StringField(choices=["SMS", "Email"])
    message_sent = BooleanField(default=False)
