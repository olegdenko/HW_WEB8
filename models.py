from mongoengine import Document, StringField, ListField, ReferenceField, EmailField, BooleanField


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField()
    best_contact_method = StringField(choices=["SMS", "Email"])
    message_sent = BooleanField(default=False)
