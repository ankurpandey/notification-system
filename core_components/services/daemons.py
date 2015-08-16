__author__ = 'arshad'


from core_components.models import EMAIL, SMS, PUSH_NOTIFICATION
from mongoengine import Q
from core_components.models.tasks import RecurringTask, SingleTask, TASK_STATUS, PENDING, COMPLETE, FAILED, PROGRESS
import datetime

def scheduled_tasks_daemon():
    from .hander import handle_message
    now = datetime.datetime.now()
    tasks = SingleTask.objects(scheduled=True).all()
    for task in tasks:
        if task.status == COMPLETE or task.status == FAILED:
            continue
        task.status = PROGRESS
        task.last_run = now
        task = task.save()
        handle_message(task)


def recurring_tasks_daemon():
    from .hander import handle_message
    now = datetime.datetime.now()
    tasks = RecurringTask.objects(Q(start__lte=now) & Q(end__gte=now)).all()
    for task in tasks:
        if (now - task.last_run).days < task.interval or task.status == COMPLETE or task.status == FAILED:
            continue
        task.last_run = now
        task.status = PROGRESS
        task = task.save()
        handle_message(task)
