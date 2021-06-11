from django.shortcuts import render
from .models import Notification
from .serializers import *

from accounts.models import *
from .views_function import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsOwner
from django.contrib.auth.decorators import permission_required
from django.db.models import Count, Q
# Create your views here.


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def notification_list(request):

    user = request.user
    noti = Notification.objects.filter(user=request.user).order_by(
        '-date_create')
    notifications = noti.all().filter(Q(turn_on=True) | Q(show=True))
    Notification.objects.filter(user=user, is_seen=False, is_open=True).update(
        is_seen=True)
    Notification.objects.filter(user=user, is_seen=False).update(is_open=True)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def turn_off_notification(request, id):

    exists, response, noti_obj = check_notification_exists(id)
    if not exists:
        return Response(status=response)

    user_obj = request.user

    if noti_obj.user != user_obj:
        return Response(
            {'stat': 'fail',
             'message': 'Notification is not for this user'},
            status=status.HTTP_403_FORBIDDEN)

    type = noti_obj.notification_type
    # fave photo
    if type == 1:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_off_notification_filter_update(1, user_obj, photo_obj=photo_obj)
        turn_off_photo_function('faved_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)
    # comment photo
    elif type == 2:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)
        turn_off_notification_filter_update(2, user_obj, photo_obj=photo_obj)
        turn_off_photo_function('comment_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)
    # reply topic
    elif type == 4:
        try:
            topic_obj = noti_obj.topic
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'topic not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_off_notification_filter_update(4, user_obj, topic_obj=topic_obj)
        topic_obj.notification = False
        topic_obj.save()
        noti_obj.show = True
        noti_obj.turn_on = False
        noti_obj.save()
        return Response(status=status.HTTP_200_OK)
    # note photo
    elif type == 5:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_off_notification_filter_update(5, user_obj, photo_obj=photo_obj)
        turn_off_photo_function('note_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)
    # invite to add your photo in group
    elif type == 6:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            group_obj = noti_obj.group
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_off_notification_filter_update(6, user_obj, photo_obj=photo_obj,
                                            group_obj=group_obj)
        turn_off_photo_function('photo_group_notification', noti_obj,
                                photo_obj)

        return Response(status=status.HTTP_200_OK)
    # your photo added to gallery
    elif type == 7:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            gallery_obj = noti_obj.gallery
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_off_notification_filter_update(7, user_obj, photo_obj=photo_obj,
                                            gallery_obj=gallery_obj)
        turn_off_photo_function('photo_gallery_notification', noti_obj,
                                photo_obj)

        return Response(status=status.HTTP_200_OK)
    # tagging photo
    elif type == 8:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_off_notification_filter_update(8, user_obj, photo_obj=photo_obj)
        turn_off_photo_function('tag_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def turn_on_notification(request, id):

    try:
        noti_obj = Notification.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response({'stat': 'fail',
                         'message': 'user not found'},
                        status=status.HTTP_404_NOT_FOUND)

    user_obj = request.user
    if noti_obj.user != user_obj:
        return Response(
            {'stat': 'fail',
             'message': 'Notification is not for this user'},
            status=status.HTTP_403_FORBIDDEN)

    type = noti_obj.notification_type
    # fave photo
    if type == 1:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_on_notification_filter_update(1, user_obj, photo_obj=photo_obj)
        turn_on_photo_function('faved_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)
    # comment photo
    elif type == 2:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)
        turn_on_notification_filter_update(2, user_obj, photo_obj=photo_obj)
        turn_on_photo_function('comment_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)
    # reply topic
    elif type == 4:
        try:
            topic_obj = noti_obj.topic
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'topic not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_on_notification_filter_update(4, user_obj, topic_obj=topic_obj)
        topic_obj.notification = True
        topic_obj.save()
        noti_obj.show = True
        noti_obj.turn_on = True
        noti_obj.save()
        return Response(status=status.HTTP_200_OK)
    # note photo
    elif type == 5:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_on_notification_filter_update(5, user_obj, photo_obj=photo_obj)
        turn_on_photo_function('note_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)
    # invite to add your photo in group
    elif type == 6:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            group_obj = noti_obj.group
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_on_notification_filter_update(6, user_obj, photo_obj=photo_obj,
                                            group_obj=group_obj)
        turn_on_photo_function('photo_group_notification', noti_obj,
                                photo_obj)

        return Response(status=status.HTTP_200_OK)
    # your photo added to gallery
    elif type == 7:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)
        try:
            gallery_obj = noti_obj.gallery
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_on_notification_filter_update(7, user_obj, photo_obj=photo_obj,
                                           gallery_obj=gallery_obj)
        turn_on_photo_function('photo_gallery_notification', noti_obj,
                               photo_obj)

        return Response(status=status.HTTP_200_OK)
    # tagging photo
    elif type == 8:
        try:
            photo_obj = noti_obj.photo
        except ObjectDoesNotExist:
            return Response({'stat': 'fail',
                             'message': 'photo not found'},
                            status=status.HTTP_404_NOT_FOUND)

        turn_on_notification_filter_update(8, user_obj, photo_obj=photo_obj)
        turn_on_photo_function('tag_notification', noti_obj, photo_obj)

        return Response(status=status.HTTP_200_OK)



# @api_view(['PUT'])
# @permission_classes((IsAuthenticated,))
# def turn_on_notification(request, id):

#     try:
#         noti_obj = Notification.objects.get(id=id)
#     except ObjectDoesNotExist:
#         return Response({'stat': 'fail',
#                          'message': 'user not found'},
#                         status=status.HTTP_404_NOT_FOUND)
#     user_obj = request.user

#     if noti_obj.user != user_obj:
#         return Response(
#             {'stat': 'fail',
#              'message': 'Notification is not for this user'},
#             status=status.HTTP_403_FORBIDDEN)

#     type = noti_obj.notification_type
#     if type == 1:
#         try:
#             photo_obj = noti_obj.photo
#         except ObjectDoesNotExist:
#             return Response({'stat': 'fail',
#                              'message': 'photo not found'},
#                             status=status.HTTP_404_NOT_FOUND)

#         turn_on_photo_function('faved_notification', noti_obj, photo_obj,
#                                user_obj)

#         return Response(status=status.HTTP_200_OK)

#     elif type == 2:
#         try:
#             photo_obj = noti_obj.photo
#         except ObjectDoesNotExist:
#             return Response({'stat': 'fail',
#                              'message': 'photo not found'},
#                             status=status.HTTP_404_NOT_FOUND)

#         turn_on_photo_function('comment_notification', noti_obj, photo_obj,
#                                user_obj)

#         return Response(status=status.HTTP_200_OK)
#     elif type == 4:
#         try:
#             topic_obj = noti_obj.topic
#         except ObjectDoesNotExist:
#             return Response({'stat': 'fail',
#                              'message': 'topic not found'},
#                             status=status.HTTP_404_NOT_FOUND)

#         topic_obj.notification = True
#         topic_obj.save()

#         noti_obj.show = True
#         noti_obj.turn_on = True
#         noti_obj.save()
#         Notification.objects.filter(topic=topic_obj, user=user_obj).update(
#             show=True, turn_on=True)
#         return Response(status=status.HTTP_200_OK)
