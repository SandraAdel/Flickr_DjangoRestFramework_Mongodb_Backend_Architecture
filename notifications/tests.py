from project.permissions import check_permission
from .serializers import *
from accounts.views import verifying_user
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *
from django.urls import reverse
from rest_framework.views import status
from .views_function import *
from accounts.views import *

# Create your tests here.


def create_test_user(email):
    # prepare user
    first_name = 'test2'
    last_name = 'name'
    age = '50'
    password = 'Kamel1234567'
    email = email
    Account.objects.create_user(email, first_name, last_name, age, password)
    user = Account.objects.get(email=email)
    verifying_user(user)
    return user


class NotificationTests(TestCase):
    def test_notification_exists(self):
        sender = create_test_user("email1")
        user = create_test_user("email2")
        notification_type = 3
        noti_obj = Notification.objects.create(
            sender=sender, user=user,
            notification_type=notification_type)
        exists, response, noti = check_notification_exists(noti_obj.id)
        self.assertEqual(exists, True)

    def test_notification_exists_failure(self):
        sender = create_test_user("email1")
        user = create_test_user("email2")
        notification_type = 3
        Notification.objects.create(
            sender=sender, user=user,
            notification_type=notification_type)
        noti_obj = Notification.objects.all().first()
        noti_obj.delete()
        exists, response, r = check_notification_exists(noti_obj.id)
        self.assertEqual(exists, False)
        self.assertEqual(response, 404)
