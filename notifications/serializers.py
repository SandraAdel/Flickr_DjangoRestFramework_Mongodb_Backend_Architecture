from rest_framework import serializers
from .models import Notification
from djongo import models
from accounts.models import *
from group.models import group, topic
from accounts.serializers import *
from photo.serializers import *
from gallery.models import Gallery


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = ['id', 'name']


class TopicSerializer(serializers.ModelSerializer):

    group = GroupSerializer(read_only=True)

    class Meta:
        model = topic
        fields = ['id', 'subject', 'group']


class GallerySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Gallery
        fields = ['owner', 'id', 'title', 'description',
                  'primary_photo_id', 'count_photos',
                  'count_comments']


class NotificationSerializer(serializers.ModelSerializer):

    photo = PhotoMetaSerializer(read_only=True)
    sender = OwnerSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    gallery = GallerySerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['sender', 'group', 'topic', 'gallery', 'photo',
                  'notification_type', 'date_create', 'is_seen']


class NotificationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id']