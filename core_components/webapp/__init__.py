__author__ = 'arshad'

from core_components.models import EMAIL, SMS, PUSH_NOTIFICATION
from core_components.models.tasks import Task, RecurringTask, SingleTask, SINGLE_TYPE, RECURRING_TASK, SCHEDULED_TYPE, PENDING
from core_components.models.messaging import MessageTemplate
from core_components.models.users import User, SystemUser, ClientUser
from flask import Flask, render_template, request, jsonify
from mongoengine import Q
import datetime, random

app = Flask(__name__, template_folder='templates', static_folder='assets', static_url_path='')

# Examples

templates = []
body = """
    <div class="container">
        <div class="row">
            <div class="col-md-4 col-md-offset-4">
                <div class="login-panel panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">Please Sign In</h3>
                    </div>
                    <div class="panel-body">
                        <form role="form">
                            <fieldset>
                                <div class="form-group">
                                    <input class="form-control" placeholder="E-mail" name="email" type="email" autofocus>
                                </div>
                                <div class="form-group">
                                    <input class="form-control" placeholder="Password" name="password" type="password" value="">
                                </div>
                                <div class="checkbox">
                                    <label>
                                        <input name="remember" type="checkbox" value="Remember Me">Remember Me
                                    </label>
                                </div>
                                <!-- Change this to a button or input when using this as a form -->
                                <a href="index.html" class="btn btn-lg btn-success btn-block">Login</a>
                            </fieldset>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""
if MessageTemplate.objects.count() is 0:
    types = [EMAIL, SMS, PUSH_NOTIFICATION]
    for i in xrange(100):
        templates.append(MessageTemplate(title='title %d' % i, subject='Test Subject Here', type=types[i % len(types)], body=body).save())

if SingleTask.objects.count() is 0:
    for i in xrange(20):
        notification_type = [EMAIL, SMS, PUSH_NOTIFICATION][i % 3]
        SingleTask(notification_type=notification_type, status=PENDING, template=MessageTemplate.objects.first(), scheduled_time=datetime.datetime.now()).save()

if RecurringTask.objects.count() is 0:
    for i in xrange(20):
        notification_type = [EMAIL, SMS, PUSH_NOTIFICATION][i % 3]
        RecurringTask(notification_type=notification_type, status=PENDING, template=MessageTemplate.objects.first(), start=datetime.datetime.now(), interval=1, end=datetime.datetime.now() + datetime.timedelta(days=random.randint(3, 100))).save()

if SystemUser.objects.count() is 0:
    for i in xrange(3):
        SystemUser.create_admin('Test Admin %d' % i, 'testing%d@mailinator.com' % i, '238238238923%d' % i, 'testing').save()

if ClientUser.objects.count() < 1000:
    for i in xrange(1000):
        ClientUser(name='Test User %d' % i, email='testing%d@mailinator.com' % i, phone='22383282%d' % i).save()

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/templates/edit/<type>/<id>')
def template_edit(type='email', id=None):
    return render_template('message_templates/edit.html', template=MessageTemplate.objects(pk=str(id)).first(), type=type)

@app.route('/templates/view/<type>/<id>')
def template_view(type='email', id=None):
   return render_template('message_templates/view.html', template=MessageTemplate.objects(pk=str(id)).first(), type=type)

@app.route('/templates/list/<type>')
def templates(type='email'):
    return render_template('message_templates/list.html', templates=MessageTemplate.objects(type=type).all(), type=type)

@app.route('/tasks/edit/<type>/<id>')
def tasks_edit(type=SINGLE_TYPE, id=None):
    return render_template('tasks/edit.html', task=Task.factory(type).objects(pk=str(id)).first(), type=type)

@app.route('/tasks/view/<type>/<id>')
def tasks_view(type=SINGLE_TYPE, id=None):
   return render_template('tasks/view.html', task=Task.factory(type).objects(pk=str(id)).first(), type=type)

@app.route('/tasks/list/<type>')
@app.route('/tasks/list/<type>/<scheduled>')
def tasks(type=SINGLE_TYPE, scheduled=None):
    if not scheduled:
        tasks = Task.factory(type).objects.all()
    else:
        tasks = Task.factory(type).objects(scheduled_time__exists=True).all()
    return render_template('tasks/list.html', tasks=tasks, type=type)

@app.route('/users/edit/<id>')
def user_edit(id=None):
    return render_template('users/edit.html', model_user=User.objects(pk=str(id)).first())

@app.route('/users/view/<id>')
def user_view(id=None):
    return render_template('users/view.html', model_user=User.objects(pk=str(id)).first())

@app.route('/users/list')
@app.route('/users/list/<type>')
def users(type=None):
    return render_template('users/list.html', users=[], type=type if type else '[All Clients]')


@app.route('/users/listing', methods=['GET', 'POST'])
def users_listing():
    print request.method
    print request.args
    draw = int(request.args.get('draw'))
    start = int(request.args.get('start'))
    size = int(request.args.get('length'))
    type = request.args.get('type')

    search = request.args.get('search[value]')

    if search and len(search) > 0:
        user_list = list(User.factory(type).objects(Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)).limit(size).skip(start).all())
    else:
        user_list = list(User.factory(type).objects.limit(size).skip(start).all())
    count = User.factory(type).objects.count()
    buttons = """
    <a href="/users/view/%s" class="btn btn-info">View</a>&nbsp;&nbsp;
    <a href="/tasks/edit/%s" class="btn btn-warning">Edit</a>&nbsp;&nbsp;
    <a href="#" class="btn btn-danger">Delete</a>
    """
    response = {
        "draw": draw,
        "recordsTotal": count,
        "recordsFiltered": count,
        "data": [[i.name, i.email, i.phone, buttons % (i.id, i.id)] for i in user_list]
    }
    print response
    return jsonify(response)

@app.route('/event-notification', methods=['POST'])
def event_notification():
    try:
        request_params = request.json()
        command = request_params.get('command')
        data = request_params.get('data')
        template_id = request_params.get('template_id')
        from ..services import event_task_listener
        task = event_task_listener(command, template_id, data)
        return jsonify(dict(status='success', message='Successfully submitted the request', task=str(task.id)))
    except Exception, e:
        return jsonify(dict(status='error', message=str(e)))
