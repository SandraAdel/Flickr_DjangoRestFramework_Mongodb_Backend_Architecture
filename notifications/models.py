from django.db import models
from djongo import models
from accounts.models import *

# Create your models here.

NOTIFICATION_TYPES = [
    (1, 'faved'),  # faved your photo
    (2, 'comment'),  # comment on you photo
    (3, 'follow'),  # follow you
    (4, 'reply'),  # reply in your topic in group
    (5, 'note'),  # note on your photo
    (6, 'group_photo_invite'),  # invite to add you photo in group
    (7, 'gallery_photo'),  # your photo added to gallery
    (8, 'tagged')  # tag you in photo
]


class Notification (models.Model):

    photo = models.ForeignKey(to='photo.Photo', on_delete=models.CASCADE,
                              related_name="noti_photo", blank=True, null=True)
    gallery = models.ForeignKey(to='gallery.Gallery', on_delete=models.CASCADE,
                                related_name="noti_gallery", blank=True,
                                null=True)
    group = models.ForeignKey(to='group.group', on_delete=models.CASCADE,
                              related_name="noti_group", blank=True, null=True)
    topic = models.ForeignKey(to='group.topic', on_delete=models.CASCADE,
                              related_name="noti_topic", blank=True, null=True)
    sender = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE,
                               related_name="noti_from_user")
    user = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE,
                             related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)

    # for turn on and off notifications
    turn_on = models.BooleanField(default=True)
    # for photo/group get turned off by user
    # it appears but with different shade
    show = models.BooleanField(default=True)
