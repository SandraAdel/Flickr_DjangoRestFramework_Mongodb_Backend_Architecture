from rest_framework import serializers
from .models import *
from accounts.serializers import *
from photo.serializers import *


class setss_serializer(serializers.ModelSerializer):
    class Meta:
        model = sets
        fields = ['title, description']


class comments_serializer(serializers.ModelSerializer):
    owner=OwnerSerializer(read_only=True)
    class Meta:
        model = commentss
        fields = '__all__'
        extra_kwargs = {'sets': {'read_only': True},'owner': {'read_only': True}}
      

class comments_serializer_post(serializers.ModelSerializer):
    
    class Meta:
        model = commentss
        fields = '__all__'
        extra_kwargs = {'sets': {'read_only': True},'owner': {'read_only': True}}
       


class sets_serializer(serializers.ModelSerializer):
    owner=OwnerSerializer(read_only=True)
    comment= comments_serializer_post(read_only=True, many=True)
    photos = PhotoSerializer(read_only=True, many=True)
    class Meta:
        model = sets
        fields = ['id', 'title', 'description', 'date_create', 'date_update',
                   'count_comments', 'can_comment', 'owner', 'primary','photos', 'comment']
       
        extra_kwargs = {'owner': {'read_only': True}}
       
class sets_serializer_post(serializers.ModelSerializer):
    
    class Meta:
        model = sets
        fields = [ 'title', 'description', 'primary']
        extra_kwargs = {'owner': {'read_only': True}}

class sets_serializer_post_swagger(serializers.ModelSerializer):
    
    class Meta:
        model = sets
        fields = [ 'title', 'description']
        extra_kwargs = {'owner': {'read_only': True}}
        