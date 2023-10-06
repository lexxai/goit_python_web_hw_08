from datetime import datetime

from mongoengine import EmbeddedDocument, Document, CASCADE, DENY
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    StringField,
    ObjectIdField,
    ReferenceField
)


class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Tag(EmbeddedDocument):
    name = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField("Authors", reverse_delete_rule=CASCADE)
    quote = StringField()
