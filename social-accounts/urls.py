from django.urls import path

from .views import FacebookLogin
app_name = "social-accounts"
urlpatterns = [
    path('facebook/', FacebookLogin.as_view(), name="fb-login"),
]
