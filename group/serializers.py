from rest_framework import serializers
from .models import *
from djongo import models
from accounts.models import *
from accounts.serializers import *

class ReplySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    class Meta:
        model = reply
        fields = '__all__'
        extra_kwargs = {'topic': {'read_only': True},
                        'owner': {'read_only': True}}

class CreateReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = reply
        fields = ['message']

class GroupMemberSerializer(serializers.ModelSerializer):

    member = OwnerSerializer(read_only=True)

    class Meta:
        model = Members
        fields = ['member', 'member_type', 'photos_count']

class GroupPendingMemberSerializer(serializers.ModelSerializer):

    pending_member = OwnerSerializer(read_only=True)

    class Meta:
        model = PendingMembers
        fields = ['pending_member', 'date_send_request', 'message']
        

class TopicSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    group_topic_reply= ReplySerializer(read_only=True, many=True)
    class Meta:
        model = topic
        fields = ['subject', 'message', 'owner', 'count_replies',
                  'date_create', 'last_edit',
                  'group_topic_reply']
        extra_kwargs = {'group': {'read_only': True},
                        'owner': {'read_only': True}}

class CreateTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = topic
        fields = ['subject', 'message']


class TopicSubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = topic
        fields = ['subject']


class TopicMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = topic
        fields = ['message']


class GroupSerializer(serializers.ModelSerializer):
    group_topic = TopicSerializer(read_only=True, many=True)

    class Meta:
        model = group
        fields = ['id', 'name', 'description', 'privacy',
                  'rules', 'eighteenplus', 'invitation_only',
                  'member_count', 'pool_count', 'date_create',
                  'topic_count', 'group_topic']
class CreateGroupSerializer(serializers.ModelSerializer):
    # group_topic = TopicSerializer(read_only=True, many=True)

    class Meta:
        model = group
        fields = [ 'name', 'description', 'privacy',
                  'eighteenplus']

class MemberGroupSerializer(serializers.ModelSerializer):

    group = GroupSerializer(read_only=True)

    class Meta:
        model = Members
        fields = ['group']


class GroupRulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = ['rules', 'rules_is_enabled']


class GroupNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = ['name', 'description']


class GroupRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = ['member_role', 'admin_role']


class GroupPrivacySerializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = ['privacy']


class GroupSafetyLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = group
        fields = ['eighteenplus']


class GroupMemberListSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Members
        fields = ['group']



