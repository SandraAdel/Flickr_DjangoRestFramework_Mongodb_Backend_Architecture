from django.db import models
from djongo import models
from djongo.models.fields import forms
from accounts.models import *
from photo.models import *

# import notifications
# from notifications.models import Notification

from django.db.models.signals import post_save, post_delete
# Create your models here.


PRIVACY_GROUP_CHOICES = [
    (1, 'private'),
    (2, 'invitation_only'),
    (3, 'public'),
]

GROUP_MEMBERS_TYPES_CHOICES = [
    (1, 'member'),
    (2, 'admin'),
]


class group (models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    rules = models.TextField(blank=True, null=True)
    rules_is_enabled = models.BooleanField(default=False)

    members = models.ManyToManyField(Account, related_name='group_member',
                                     through='Members')
    member_count = models.PositiveIntegerField(default=1)

    pending_members = models.ManyToManyField(
        Account, related_name='group_pending_member', through='PendingMembers',
        blank=True)
    pending_members_count = models.IntegerField(default=0)

    pool_count = models.PositiveIntegerField(default=0)
    topic_count = models.PositiveIntegerField(default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    privacy = models.PositiveIntegerField(choices=PRIVACY_GROUP_CHOICES)
    eighteenplus = models.BooleanField(default=False)
    invitation_only = models.BooleanField(default=False)

    photos = models.ManyToManyField(
        Photo, related_name='group_photos', blank=True)

    member_role = models.TextField(default="Member", blank=True)
    admin_role = models.TextField(default="Admin", blank=True)

    def __str__(self):
        return self.name


class Members (models.Model):
    group = models.ForeignKey(group, related_name='group_join',
                              on_delete=models.CASCADE)
    member = models.ForeignKey(Account, on_delete=models.CASCADE,
                               related_name='member_join')
    member_type = models.PositiveIntegerField(choices=GROUP_MEMBERS_TYPES_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    photos_count = models.PositiveIntegerField(default=0)
    topic_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [['group', 'member']]


class PendingMembers (models.Model):
    group = models.ForeignKey(group, related_name='group_join_request',
                              on_delete=models.CASCADE)
    pending_member = models.ForeignKey(Account, on_delete=models.CASCADE,
                                       related_name='member_join_request')
    date_send_request = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)

    class Meta:
        unique_together = [['group', 'pending_member']]


class topic(models.Model):
    group = models.ForeignKey(group, related_name='group_topic',
                              on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,
                              related_name='topic_owner')
    count_replies = models.PositiveIntegerField(default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    is_sticky = models.BooleanField(default=False)

    # check if this topic notification is turn on or off
    notification = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


class reply(models.Model):
    topic = models.ForeignKey(topic, related_name='group_topic_reply',
                              on_delete=models.CASCADE)
    message = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE,
                              related_name='reply_owner')
    date_create = models.DateTimeField(auto_now_add=True)
    lastedit = models.DateTimeField(auto_now=True)

    def member_reply_topic_add(sender, instance, *args, **kwargs):
        reply = instance
        topic = reply.topic
        text_preview = reply.message
        sender = reply.owner
        if sender != topic.owner:
            if topic.notification:
                turn_on = True
                show = True
            else:
                turn_on = False
                show = False
            notify = Notification(topic=topic, sender=sender, user=topic.owner,
                                  text_preview=text_preview, turn_on=turn_on,
                                  notification_type=4, show=show)
            notify.save()

    def member_reply_topic_remove(sender, instance, *args, **kwargs):
        reply = instance
        topic = reply.topic
        text_preview = reply.message
        sender = reply.owner
        if sender != topic.owner:
            notify = Notification.objects.filter(topic=topic, sender=sender,
                                                 user=topic.owner,
                                                 text_preview=text_preview,
                                                 notification_type=4)
            notify.delete()

    def __str__(self):
        return self.message


# # Reply
post_save.connect(reply.member_reply_topic_add, sender=reply)
post_delete.connect(reply.member_reply_topic_remove, sender=reply)
