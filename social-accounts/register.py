from django.contrib.auth import authenticate
from accounts.models import *
from rest_framework.exceptions import AuthenticationFailed



def login_social_user(email):
    filtered_user_by_email = Account.objects.filter(email=email)
    if filtered_user_by_email.exists():
        
        user = Account.objects.get(email=email)         
        user.login_from='facebook'
        user.save()
        return {
            'username': user.username,
            'email': user.email,
            'tokens': user.tokens()}

    else:
        
        raise AuthenticationFailed(
            detail= ' You dont have account on Fotone !')


