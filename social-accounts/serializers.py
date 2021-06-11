from rest_framework import serializers
from . import facebook
from .register import login_social_user
import os
from rest_framework.exceptions import AuthenticationFailed


class FacebookLoginSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            email = user_data['email'] 
            stat= login_social_user(
                email=email,
            )
            
            return stat
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )

