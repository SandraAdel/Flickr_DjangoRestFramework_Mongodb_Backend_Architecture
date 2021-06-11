from django.db import models
from django.utils import timezone
from accounts.models import *
from photo.models import *


class sets(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_photoset')
    photos = models.ManyToManyField(
        Photo, related_name='sets_photos', blank=True)
    primary = models.PositiveIntegerField( blank=True) #primary photo
    count_photos = models.PositiveIntegerField(default=1) #photos counter
    count_comments = models.PositiveIntegerField(default=0) #comments counter
    can_comment = models. BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True) #date of creation
    date_update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models. TextField(max_length=1000, blank=True)
    
    def __str__(self):
        return self.title


class commentss(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, 
    related_name='user_photoset_comments')
    contents = models.CharField(max_length=1000) # the text
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    sets = models.ForeignKey(sets, related_name='comment', 
                             on_delete=models.CASCADE)
    
    