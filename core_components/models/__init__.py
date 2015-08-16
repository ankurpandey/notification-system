__author__ = 'arshad'

import datetime
from mongoengine import *

conn = connect('notification_system')
print 'Connection Object', conn

MESSAGE_STATUS_CHOICES = (WAITING, SENT, DISCARDED) = ('waiting', 'sent', 'discarded')
MESSAGE_TYPE = (EMAIL, SMS, PUSH_NOTIFICATION) = ('email', 'sms', 'push_notification')

class Node(object):
    created  = DateTimeField(default=datetime.datetime.now, required=True)
    modified = DateTimeField(default=datetime.datetime.now, required=True)


class Configuration(Document):
    meta = {'allow_inheritance': True}

class EmailConfiguration(Configuration):
    pass

class SMSConfiguration(Configuration):
    pass

class PushNotiticationConfiguration(Configuration):
    pass
