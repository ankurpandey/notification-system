__author__ = 'arshad'

from core_components.models import EMAIL, SMS, PUSH_NOTIFICATION
from core_components.models.tasks import FAILED


def handle_message(task):
    from core_components.modules.email_module import send_emails
    from core_components.modules.sms_module import send_sms
    from core_components.modules.push_notification_module import send_push_notification
    command = task.notification_type
    if command == EMAIL:
        send_emails(str(task.id))
    elif command == SMS:
        send_sms()
    elif command == PUSH_NOTIFICATION:
        send_push_notification()
    else:
        task.status = FAILED
        task.status_message = str('Invalid command')
        task.save()
        raise Exception('Invalid command')



