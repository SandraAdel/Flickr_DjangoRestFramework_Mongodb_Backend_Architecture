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


class TestModels(TestCase):
    def test_model_str(self):
        user = create_test_user("email")
        group_obj = group.objects.create(name="New Group")
        topic_obj = topic.objects.create(subject="New topic", owner=user)
        reply_obj = reply.objects.create(message="New message",
                                         topic=topic_obj, owner=user)
        self.assertEqual(str(group_obj), "New Group")
        self.assertEqual(str(topic_obj), "New topic")
        self.assertEqual(str(reply_obj), "New message")


class GroupSerializerTests(TestCase):

    def test_create_group_success(self):
        # prepare group data
        data = {}
        name = 'group test'
        privacy = 1
        for variable in ["name", "privacy"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateGroupSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_group_missing_name(self):
        # prepare group data
        data = {}
        privacy = 1
        for variable in ["privacy"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateGroupSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['name'][0],
                         'This field is required.')

    def test_create_group_missing_privacy(self):
        # prepare group data
        data = {}
        name = 'group test'
        for variable in ["name"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateGroupSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['privacy'][0],
                         'This field is required.')

    def test_create_group_exceeds_name(self):
        # prepare group data
        data = {}
        name = ''
        for i in range (101):
            name = name + 's'
        privacy = 1
        for variable in ["name", "privacy"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateGroupSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['name'][0],
                         'Ensure this field has no more than 100 characters.')

    def test_create_group_name_already_exists(self):
        # prepare already exist group
        name = 'group test'
        privacy = 1
        group.objects.create(name=name, privacy=privacy)

        # prepare test data
        data = {}
        name = 'group test'
        privacy = 1
        for variable in ["name", "privacy"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateGroupSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['name'][0],
                         'group with this name already exists.')

    def test_change_group_name(self):
        # prepare group data
        data = {}
        name = 'group test'
        description = 'description'
        privacy = 1
        group.objects.create(name=name, privacy=privacy,
                             description=description)

        group_obj = group.objects.get(name=name)
        data = {}
        name = "new group"
        for variable in ["name"]:
            data[variable] = eval(variable)
        changed_serializer = GroupNameSerializer(group_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = group.objects.get(name=name)
        self.assertEqual(obj.name, 'new group')

    def test_change_group_description(self):
        # prepare group data
        data = {}
        name = 'group test'
        description = 'description'
        privacy = 1
        group.objects.create(name=name, privacy=privacy,
                             description=description)

        group_obj = group.objects.get(name=name)
        data = {}
        name = "group test"
        description = 'new description'
        for variable in ["name", "description"]:
            data[variable] = eval(variable)
        changed_serializer = GroupNameSerializer(group_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = group.objects.get(name=name)
        self.assertEqual(obj.description, 'new description')

    def test_change_group_privacy(self):
        # prepare group data
        data = {}
        name = 'group test'
        privacy = 1
        group.objects.create(name=name, privacy=privacy)

        group_obj = group.objects.get(name=name)
        data = {}
        privacy = 2
        for variable in ["privacy"]:
            data[variable] = eval(variable)
        changed_serializer = GroupPrivacySerializer(group_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = group.objects.get(name=name)
        self.assertEqual(obj.privacy, 2)

    def test_change_group_safety_level(self):
        # prepare group data
        data = {}
        name = 'group test'
        privacy = 1
        eighteenplus = False
        group.objects.create(name=name, privacy=privacy,
                             eighteenplus=eighteenplus)

        group_obj = group.objects.get(name=name)
        data = {}
        eighteenplus = True
        for variable in ["eighteenplus"]:
            data[variable] = eval(variable)
        changed_serializer = GroupSafetyLevelSerializer(group_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = group.objects.get(name=name)
        self.assertEqual(obj.eighteenplus, True)

    def test_change_group_rules(self):
        # prepare group data
        data = {}
        name = 'group test'
        privacy = 1
        rules = 'rules'
        group.objects.create(name=name, privacy=privacy,
                             rules=rules)

        group_obj = group.objects.get(name=name)
        data = {}
        rules = 'new rules'
        for variable in ["rules"]:
            data[variable] = eval(variable)
        changed_serializer = GroupRulesSerializer(group_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = group.objects.get(name=name)
        self.assertEqual(obj.rules, 'new rules')

    def test_change_group_roles(self):
        # prepare group data
        data = {}
        name = 'group test'
        privacy = 1
        member_role = 'member_role'
        admin_role = 'admin_role'
        group.objects.create(name=name, privacy=privacy,
                             member_role=member_role,
                             admin_role=admin_role)

        group_obj = group.objects.get(name=name)
        data = {}
        member_role = 'new member_role'
        admin_role = 'new admin_role'
        for variable in ["member_role", "admin_role"]:
            data[variable] = eval(variable)
        changed_serializer = GroupRoleSerializer(group_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = group.objects.get(name=name)
        self.assertEqual(obj.member_role, 'new member_role')
        self.assertEqual(obj.admin_role, 'new admin_role')

    def test_delete_group(self):
        # prepare group data
        data = {}
        name = 'group test'
        privacy = 1
        for variable in ["name", "privacy"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateGroupSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        group_obj = group.objects.get(name=name)
        group_obj.delete()
        deleted_obj = group.objects.filter(name=name)
        self.assertEqual(deleted_obj.exists(), False)


class TopicSerializerTests(TestCase):

    def test_create_topic_success(self):
        # prepare topic data
        data = {}
        subject = 'subject test'
        message = 'message test'
        for variable in ["subject", "message"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateTopicSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_topic_missing_subject(self):
        # prepare topic data
        data = {}
        message = 'message test'
        for variable in ["message"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateTopicSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['subject'][0],
                         'This field is required.')

    def test_create_topic_missing_message(self):
        # prepare topic data
        data = {}
        subject = 'subject test'

        for variable in ["subject"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateTopicSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['message'][0],
                         'This field is required.')

    def test_create_topic_exceeds_subject(self):
        # prepare group data
        data = {}
        subject = ''
        for i in range (101):
            subject = subject + 's'
        message = 'message test'
        for variable in ["subject", "message"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateTopicSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['subject'][0],
                         'Ensure this field has no more than 100 characters.')

    def test_change_topic_subject(self):
        # prepare group data
        data = {}
        subject = 'subject test'
        message = 'message test'
        topic.objects.create(subject=subject, message=message)

        topic_obj = topic.objects.get(subject=subject)
        data = {}
        subject = "new subject"
        for variable in ["subject"]:
            data[variable] = eval(variable)
        changed_serializer = TopicSubjectSerializer(topic_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = topic.objects.get(subject=subject)
        self.assertEqual(obj.subject, 'new subject')

    def test_change_topic_message(self):
        # prepare group data
        data = {}
        subject = 'subject test'
        message = 'message test'
        topic.objects.create(subject=subject, message=message)

        topic_obj = topic.objects.get(subject=subject)
        data = {}
        message = 'new message'
        for variable in ["message"]:
            data[variable] = eval(variable)
        changed_serializer = TopicMessageSerializer(topic_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = topic.objects.get(subject=subject)
        self.assertEqual(obj.message, 'new message')

    def test_delete_topic(self):
        # prepare group data
        data = {}
        subject = 'subject test'
        message = 'message test'
        for variable in ["subject", "message"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateTopicSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        topic_obj = topic.objects.get(subject=subject)
        topic_obj.delete()
        deleted_obj = topic.objects.filter(subject=subject)
        self.assertEqual(deleted_obj.exists(), False)


class ReplySerializerTests(TestCase):

    def test_create_reply_success(self):
        # prepare reply data
        data = {}
        message = 'message test'
        for variable in ["message"]:
            data[variable] = eval(variable)

        # Sending data to serializer to test serializer
        serializer = CreateReplySerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_reply_missing_message(self):
        # prepare reply data
        data = {}

        # Sending data to serializer to test serializer
        serializer = CreateReplySerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['message'][0],
                         'This field is required.')

    def test_change_reply_message(self):
        # prepare reply data
        subject = 'subject test'
        message = 'message test'
        user = create_test_user("email")
        topic_obj = topic.objects.create(subject=subject, message=message,
                                         owner=user)

        data = {}
        message = 'message test'
        reply.objects.create(message=message, topic=topic_obj, owner=user)

        reply_obj = reply.objects.get(message=message)
        data = {}
        message = 'new message'
        for variable in ["message"]:
            data[variable] = eval(variable)
        changed_serializer = CreateReplySerializer(reply_obj, data=data)
        changed_serializer.is_valid()
        changed_serializer.save()

        obj = reply.objects.get(message=message)
        self.assertEqual(obj.message, 'new message')

    def test_delete_reply(self):
        # prepare reply data
        subject = 'subject test'
        message = 'message test'
        user = create_test_user("email")
        topic_obj = topic.objects.create(subject=subject, message=message,
                                         owner=user)

        message = 'message test'
        reply.objects.create(message=message, topic=topic_obj, owner=user)

        reply_obj = reply.objects.get(message=message)
        reply_obj.delete()
        deleted_obj = reply.objects.filter(message=message)
        self.assertEqual(deleted_obj.exists(), False)

