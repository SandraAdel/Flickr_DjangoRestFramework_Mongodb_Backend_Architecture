"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings              
from django.conf.urls.static import static


schema_view = get_schema_view(
    
    openapi.Info(
        title="Flicker API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url='https://www.fotone.me/api/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/postman', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/social-accounts/', include('social-accounts.urls',
                                        namespace="social_accounts")),
    path('api/admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    # path('api/profiles/', include('profiles.urls', namespace='profiles')),
    path('api/gallery/', include('gallery.urls', namespace='gallery')),
    path('api/photos/', include('photo.urls', namespace='photos')),
    path('api/photosets/', include('photosets.urls', namespace='photosets')),
    path('api/group/', include('group.urls', namespace='group')),
    path('api/notifications/', include('notifications.urls',
                                   namespace='notifications')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
