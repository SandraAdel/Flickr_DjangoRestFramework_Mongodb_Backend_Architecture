from rest_framework import serializers
from .models import *
from accounts.serializers import *
from photo.serializers import *

# Serializers define the API representation.
class CommentSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    class Meta:
        model = Comments
        # total info for a comment on a gallery
        fields = '__all__'
        extra_kwargs = {
            'gallery': {'read_only': True}, 'owner': {'read_only': True}}

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        # total info for a comment on a gallery
        fields = '__all__'
        extra_kwargs = {
            'gallery': {'read_only': True}, 'owner': {'read_only': True}}
class GallerySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    # photos = PhotoSerializer(read_only=True, many=True)
    # comments= CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Gallery
        # total info for a gallery
        fields = [
            'id', 'title', 'description', 'date_create', 'date_update',
            'count_media','count_comments', 'comments',
            'owner', 'photos', 'primary_photo_id']
        extra_kwargs = {'owner': {'read_only': True}}

class CreateGallerySerializer(serializers.ModelSerializer):
    # owner = OwnerSerializer(read_only=True)
    class Meta:
        model = Gallery
        # specific info for a gallery needed to create and edit the gallery
        fields = [
            'id', 'title', 'description', 'owner',
             'primary_photo_id','photos']
        extra_kwargs = {'owner': {'read_only': True},'photos':{'read_only':True},'primary_photo_id':{'read_only': True}}
        


