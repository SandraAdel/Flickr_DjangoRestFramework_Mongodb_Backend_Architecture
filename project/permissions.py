from rest_framework import permissions
from rest_framework import status


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
 
def check_permission( user, obj):
    bool=True
    response=''
    if not (obj.owner == user) :
        response=status.HTTP_403_FORBIDDEN
        bool=False    
    return bool, response