from django.db import models
from accounts.models import *
from photo.models import *

# Create your models here.


class Gallery(models.Model):
    # user who created the gallery, one user has many galleries
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='user_galleries')
    # photos inside the gallery ,
    #  one gallery can have many photos and one photo can be in many galleries
    photos = models.ManyToManyField(
        Photo, related_name='gallery_photos', blank=True)
    # if the gallery is empty the primary photo id is set to null
    # otherwise it wil be the id of the first item added to the gallery
    primary_photo_id = models.PositiveIntegerField(blank=True)
    # title is required while description is optional
    title = models.CharField(max_length=100,)
    description = models.TextField(max_length=1000, blank=True)
    # dates automatically filled
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # no of items in the gallery
    count_media = models.PositiveIntegerField(default=0)
    count_comments = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comments(models.Model):
    # user who created the comment, one user can make many comments
    owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE, related_name='user_gallery_comments')
    # the gallery where comment belongs, one gallery can have many comments
    gallery = models.ForeignKey(
        Gallery, related_name='comments', on_delete=models.CASCADE)
    # text of the comment
    content = models.TextField(max_length=1000)
    # dates automatically filled
    date_create = models.DateTimeField(auto_now=True)
    date_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
