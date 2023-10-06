from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField



class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()    
    description = StringField()
    

class Tag(EmbeddedDocument):
    name = StringField()


class Quotes(Document):
    # tags = ListField(EmbeddedDocumentField(Tag))
    tags = ListField(StringField())
    author = StringField()
    quote = StringField()


