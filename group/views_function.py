from .models import *
from accounts.models import Account
from django.db.models import Count


def group_obj_increment(group_obj, field_increment):
    """
    Increment group items
    
    :param name: obj : group 
    :param type: group object
    :param name: field increment
    :param type: string
    :return: None
    """
    if field_increment == 'member_count':
        group_obj.member_count += 1
    elif field_increment == 'pending_members_count':
        group_obj.pending_members_count += 1
    group_obj.save()


def group_obj_decrement(group_obj, field_decrement):
    """
    Decrement group items
    
    :param name: obj : group 
    :param type: group object
    :param name: field decrement
    :param type: string
    :return: None
    """
    if field_decrement == 'member_count':
        group_obj.member_count -= 1
    elif field_decrement == 'pending_members_count':
        group_obj.pending_members_count -= 1
    group_obj.save()


def group_privacy_invitation(request, group_obj, serializer, condition):
    """
    Check group privacy and set group invitation only
    
    :param name: obj : group 
    :param type: group object
    :param name: serializer
    :param type: object
    :param name: condition
    :param type: int
    :return: int
    """
    if condition == 1:
        if group_obj.privacy == 1 and (serializer.validated_data['privacy'] == 2 or serializer.validated_data['privacy'] == 3):
            return 2

        if group_obj.privacy == 2 and (serializer.validated_data['privacy'] == 1 or serializer.validated_data['privacy'] == 3):
            group_obj.invitation_only = False

    elif serializer.validated_data['privacy'] == 1 or serializer.validated_data['privacy'] == 3:
        group_obj.invitation_only = False

    elif serializer.validated_data['privacy'] == 2:
        group_obj.invitation_only = True

    if condition == 1:
        group_obj.privacy = request.data['privacy']
        return 1

    group_obj.save()


def member_exists(request, group_obj):
    """
    Check if a member exist

    :param name: obj : group 
    :param type: group object
    :param name: obj : request.user 
    :param type: user object
    :return name: bool : Does member exist?
    :return type: bool
    """
    members = Members.objects.filter(group=group_obj,
                                     member=request.user).count()
    if members > 0:
        exist = True
    else:
        exist = False
    return exist


def limit_groups_number(groups, max_limit):
    """
    limit groups number

    :param name: groups 
    :param type: group object
    :param name: max limit
    :param type: int
    :return name: groups
    :return type: group object
    """
    required_groups_ids_list = []
    count = 1
    for group1 in groups:
        if count <= max_limit:
            required_groups_ids_list.append(group1.id)
            count += 1

    required_groups = group.objects.filter(
        id__in=required_groups_ids_list).order_by('-date_create')
    return required_groups