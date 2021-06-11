from .models import *
from accounts.models import Account
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

def check_notification_exists(id):
    """
    Check if notification exists

    :param name: group id  
    :param type: int
    :return name: bool : Does cnotification exist?
    :return type: bool
    :return name: Response 
    :return name: notification : notification returned
    :return type: notification object
    """
    noti_obj=None
    response = ''
    bool = False
    try:
        noti_obj = Notification.objects.get(id=id)
        bool = True
    except ObjectDoesNotExist:
        response = status.HTTP_404_NOT_FOUND
    return bool, response, noti_obj


def turn_off_notification_filter_update(noti_type, user_obj,
                                        group_obj=None, gallery_obj=None,
                                        topic_obj=None, photo_obj=None):
    """
    turn off notification 

    :param name: notification type
    :param type: int
    :param name: obj : user 
    :param type: user object
    :param name: obj : group 
    :param type: group object
    :param name: obj : gallery 
    :param type: gallery object
    :param name: obj : topic
    :param type: topic object
    :param name: obj : photo 
    :param type: photo object
    :returns: None
    """
    if noti_type == 1 | noti_type == 2 | noti_type == 5 | noti_type == 8:
        Notification.objects.filter(photo=photo_obj, user=user_obj).update(
            show=False, turn_on=False)
    elif noti_type == 4:
        Notification.objects.filter(topic=topic_obj, user=user_obj).update(
            show=False, turn_on=False)
    elif noti_type == 6:
        Notification.objects.filter(user=user_obj, group_obj=group_obj,
                                    photo=photo_obj).update(
                                        show=False, turn_on=False)
    elif noti_type == 7:
        Notification.objects.filter(gallery=gallery_obj, user=user_obj,
                                    photo=photo_obj).update(
                                        show=False, turn_on=False)
    return


def turn_off_photo_function(notification, noti_obj, photo_obj):
    """
    turn off photo notification 

    :param name: notification field
    :param type: string
    :param name: obj : notification
    :param type: notification object
    :param name: obj : photo 
    :param type: photo object
    :returns: None
    """
    if notification == 'faved_notification':
        photo_obj.faved_notification = False
    elif notification == 'comment_notification':
        photo_obj.comment_notification = False
    elif notification == 'note_notification':
        photo_obj.note_notification = False
    elif notification == 'tag_notification':
        photo_obj.tag_notification = False
    elif notification == 'photo_gallery_notification':
        photo_obj.photo_gallery_notification = False
    elif notification == 'photo_group_notification':
        photo_obj.photo_group_notification = False
    photo_obj.save()

    noti_obj.show = True
    noti_obj.turn_on = False
    noti_obj.save()


def turn_on_notification_filter_update(noti_type, user_obj,
                                       group_obj=None, gallery_obj=None,
                                       topic_obj=None, photo_obj=None):
    """
    turn on notification 

    :param name: notification type
    :param type: int
    :param name: obj : user 
    :param type: user object
    :param name: obj : group 
    :param type: group object
    :param name: obj : gallery 
    :param type: gallery object
    :param name: obj : topic
    :param type: topic object
    :param name: obj : photo 
    :param type: photo object
    :returns: None
    """
    if noti_type == 1 | noti_type == 2 | noti_type == 5 | noti_type == 8:
        Notification.objects.filter(photo=photo_obj, user=user_obj).update(
            show=True, turn_on=True)
    elif noti_type == 4:
        Notification.objects.filter(topic=topic_obj, user=user_obj).update(
            show=True, turn_on=True)
    elif noti_type == 6:
        Notification.objects.filter(group=group_obj, user=user_obj,
                                    photo=photo_obj).update(
                                        show=True, turn_on=True)
    elif noti_type == 7:
        Notification.objects.filter(gallery=gallery_obj, user=user_obj,
                                    photo=photo_obj).update(
                                        show=True, turn_on=True)


def turn_on_photo_function(notification, noti_obj, photo_obj):
    """
    turn on photo notification 

    :param name: notification field
    :param type: string
    :param name: obj : notification
    :param type: notification object
    :param name: obj : photo 
    :param type: photo object
    :returns: None
    """
    if notification == 'faved_notification':
        photo_obj.faved_notification = True
    elif notification == 'comment_notification':
        photo_obj.comment_notification = True
    elif notification == 'note_notification':
        photo_obj.note_notification = True
    elif notification == 'tag_notification':
        photo_obj.tag_notification = True
    elif notification == 'photo_gallery_notification':
        photo_obj.photo_gallery_notification = True
    elif notification == 'photo_group_notification':
        photo_obj.photo_group_notification = True
    photo_obj.save()

    noti_obj.show = True
    noti_obj.turn_on = True
    noti_obj.save()