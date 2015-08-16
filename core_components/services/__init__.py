__author__ = 'arshad'

import datetime
from core_components.models.tasks import SingleTask, PENDING, SINGLE_TYPE, RECURRING_TASK, RecurringTask
from core_components.models.messaging import MessageTemplate
from bson import ObjectId

def get_template(template):
    if isinstance(template, MessageTemplate):
        return template
    if type(template) in [str, unicode, ObjectId]:
        return MessageTemplate.objects(pk=str(template)).first()
    else:
        return None

def event_task_listener(notification_type, template, data):
    from .hander import handle_message
    template = get_template(template)
    task = SingleTask(status=PENDING, template=template, notification_type=notification_type, filters=data).save()
    handle_message(task)
    return task


def create_scheduled_task(notification_type, template, trigger_time, data):
    template = get_template(template)
    return SingleTask(status=PENDING,template=template,  notification_type=notification_type, filters=data, scheduled_time=trigger_time).save()


def create_recurring_task(notification_type, template, interval, start, end, data):
    template = get_template(template)
    return RecurringTask(status=PENDING,template=template,  notification_type=notification_type, filters=data, interval=interval, start=start, end=end).save()
