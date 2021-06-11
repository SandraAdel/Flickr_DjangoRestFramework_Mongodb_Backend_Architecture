from django.urls import path, include
from notifications import views
app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:id>/turn-off', views.turn_off_notification, name='turn_off_notification'),
    path('<int:id>/turn-on', views.turn_on_notification, name='turn_on_notification'),
]
