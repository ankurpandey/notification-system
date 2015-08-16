__author__ = 'arshad'

from mongoengine import *
from . import *
import hashlib

class User(Node,Document):
    email = StringField(required=True)
    name = StringField(max_length=50)
    phone = StringField()

    meta = {'allow_inheritance': True}

    def notification_preferences(self):
        return UserNotificationPreferences.objects.order_by('-modified').all()

    def update_preference(self, email_enabled, sms_enabled, push_enabled):
        return UserNotificationPreferences(email_enabled=email_enabled, sms_enabled=sms_enabled, push_enabled=push_enabled).save()

    @classmethod
    def factory(cls, type):
        if type == 'system':
            return SystemUser
        else:
            return ClientUser

class UserNotificationPreferences(Node, Document):
    user = ReferenceField('User')
    email_enabled = BooleanField(default=True)
    sms_enabled = BooleanField(default=True)
    push_enabled = BooleanField(default=True)


class SystemUser(User):
    passwd = StringField()
    email_configurations = ListField(ReferenceField('Configuration'))
    sms_configurations = ListField(ReferenceField('Configuration'))
    push_notification_configurations = ListField(ReferenceField('Configuration'))

    @property
    def password(self):
        return self.passwd

    @password.setter
    def password(self, new_password):
        self.passwd = hashlib.md5(new_password).hexdigest()

    @classmethod
    def authenticate(self, email, password):
        user = SystemUser.objects(email__iexact=email).first()
        if user and user.password == hashlib.md5(password).hexdigest():
            return True
        return False

    @classmethod
    def create_admin(cls, name, email, phone, password):
        user = SystemUser(name=name,email=email, phone=phone)
        user.password = password
        return user.save()


class ClientUser(User):
    properties = DictField()

    @classmethod
    def create_admin(cls, name, email, phone, **kwargs):
        user = ClientUser(name=name,email=email, phone=phone)
        for k, v in kwargs.iteritems():
            user.properties[k]=v
        return user.save()

    @classmethod
    def get_all_by_filter(cls, **kwargs):
        filters = {}
        for k, v in kwargs.iteritems():
            if any(u in k for u in ['name', 'email', 'phone']):
                filters[k] = v
            else:
                filters["properties__%s" % k] = v
        return ClientUser.objects(**filters).all()



    @classmethod
    def update_user(cls, name, email, phone, **kwargs):
        pass

    @classmethod
    def upload_csv(cls, csv_lines):
        pass