__author__ = 'arshad'

from mongoengine import *
from . import EMAIL, SMS, PUSH_NOTIFICATION, Node
import datetime

TASK_TYPES = (RECURRING_TASK, SINGLE_TYPE, SCHEDULED_TYPE) = ('recurring', 'single', 'scheduled')
TASK_STATUS = (PENDING, COMPLETE, FAILED, PROGRESS) = ['PENDING', 'COMPLETE', 'FAILED', 'PROGRESS']

class Task(Node, Document):
    status = StringField(choices=TASK_STATUS)
    notification_type = StringField(choices=[EMAIL, SMS, PUSH_NOTIFICATION])
    filters = DictField()
    template = ReferenceField('MessageTemplate')

    status_message = StringField()

    meta = {'allow_inheritance': True}

    @classmethod
    def factory(cls, type):
        if str(type) == SINGLE_TYPE:
            return SingleTask
        elif str(type) == RECURRING_TASK:
            return RecurringTask
        else:
            return Task

class SingleTask(Task):
    task_type = StringField(default=SINGLE_TYPE)
    scheduled_time = DateTimeField(default=datetime.datetime.now)

class RecurringTask(Task):
    task_type = StringField(default=RECURRING_TASK)
    interval = IntField(default=1)
    start   = DateTimeField()
    end     = DateTimeField()
    last_run = DateTimeField()
