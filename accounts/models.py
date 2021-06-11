from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from notifications.models import Notification
from django.db.models.signals import post_save, post_delete
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email,first_name ,last_name , age, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not age:
            raise ValueError('Users must have an age')
        
        username=email.split('@')[0].lower()
        user = self.model(
            
            email=email.lower(),
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name='admin' ,last_name='admin',age='0'):
        username=email.split('@')[0].lower()
        user = self.create_user(
            email=email.lower(),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_pro = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField( max_length=16,db_index=True)
    first_name = models.CharField(verbose_name='first-name', max_length=60)
    last_name = models.CharField(verbose_name='last-name', max_length=60)
    age = models.PositiveIntegerField( validators=[
            MaxValueValidator(110),
            MinValueValidator(10)
        ],default=0)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_pro = models.BooleanField(default=False)
    is_followed=models.BooleanField(default=False)
    total_media= models.PositiveIntegerField(default=0)
    fav_count = models.PositiveIntegerField(default=0)
    count_groups = models.PositiveIntegerField(default=0)
    tag_count = models.PositiveIntegerField(default=0)
    galleries_count = models.PositiveIntegerField(default=0)
    photosets_count = models.PositiveIntegerField(default=0)
    profile_pic = models.ImageField(upload_to="images/",null=True , blank=True)
    cover_photo= models.ImageField(upload_to="images/",null=True , blank=True)
    followers_count = models.PositiveIntegerField(default=0, null=True)
    following_count = models.PositiveIntegerField(default=0, null=True)
    login_from = models.CharField(
        max_length=255, blank=False,
        null=False, default="email")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app?
    def has_module_perms(self, app_label):
        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Contacts(models.Model):
    # table to represent the following-followers system
    user = models.ForeignKey(Account, related_name='follow_follower', on_delete=models.CASCADE, editable=False)
    followed = models.ForeignKey(Account, related_name='follow_followed', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)

    
    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.user
        followed = follow.followed

        notify = Notification(sender=sender, user=followed,
                              notification_type=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.user
        followed = follow.followed

        notify = Notification.objects.filter(sender=sender, user=followed,
                                             notification_type=3)
        notify.delete()


# follow a user
post_save.connect(Contacts.user_follow, sender=Contacts)
post_delete.connect(Contacts.user_unfollow, sender=Contacts)


class PlayerIds(models.Model):
    user = models.ForeignKey(Account, related_name='account_player_id',
                             on_delete=models.CASCADE)
    player_id = models.CharField(max_length=50)