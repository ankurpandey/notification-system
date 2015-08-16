__author__ = 'arshad'

from mongoengine import *
from . import Node, MESSAGE_STATUS_CHOICES, MESSAGE_TYPE

PUSH_NOTIFICATION_TYPES = (ANDROID_PUSH_NOTIFICATION, IPHONE_PUSH_NOTIFICATION, BLACKBERRY_PUSH_NOTIFICATION, LUMIA_PUSH_NOTIFICATION) = ('android', 'iphone', 'blackberry', 'lumia')

class MessageTemplate(Node, Document):
    title = StringField()
    subject = StringField()
    body = StringField()
    type = StringField(choices=MESSAGE_TYPE)

    meta = {'allow_inheritance': True}


class Message(Node):
    recipient = ReferenceField('User')
    sender = ReferenceField('User')
    subject = StringField(required=True)
    body = StringField()
    status = StringField(choices=MESSAGE_STATUS_CHOICES)
    template = ReferenceField('MessageTemplate')
    task = ReferenceField('Task')
    subject = StringField()
    body = StringField()


class Email(Message, Document):
    from_address = StringField()
    to_address = StringField()

class SMS(Message):
    phone_number = StringField()

class PushNotification(Message, Document):
    notification_type = StringField(choices=PUSH_NOTIFICATION_TYPES)

