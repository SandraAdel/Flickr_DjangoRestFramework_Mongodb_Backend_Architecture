from . import views
from django.urls import path, include
app_name = 'gallery'
urlpatterns = [
    # get , edit and delete a specific gallery APIs
    path('<int:galpk>/info', views.gallery_info, name='gallery-info'),

   # edit and delete a specific gallery APIs
    path('<int:galpk>', views.edit_or_delete_gallery, name='edit_or_delete_gallery'),
    # get list of galleries or create a new one APIS

    path('', views.gallery_list, name='gallery-list'),

    # search for a gallery by its title API
    path('search', views.find_gallery,  name='gallery-search'),

    # get list of comments to a specific gallery APIs
    path('<int:galpk>/comments-list', views.gallery_comments_list,
         name='gallery-comments-list'),

    path('<int:galpk>/comment', views.create_gallery_comment,
          name='create_gallery_comment'),
    # get ,edit and delete a specific comment on a gallery APIs
    path('<int:galpk>/comment/<int:compk>', views.gallery_comment,
         name='gallery-comment-info'),

    # get the photos list in a specific gallery API
    path('<int:galpk>/photos', views.gallery_photos,
         name='gallery_photos'),

    # get the list of galleries in which a specific photo is added API
    path('photos-in/<int:phopk>', views.photo_galleries,
         name='photo_galleries'),
    path('photos/<int:phopk>', views.create_gallery_with_primary_photo,
         name='create_gallery_with_primary_photo'),    

    # add or remove a specific photo in a specific gallery APIs
    path('<int:galpk>/photos/<int:phopk>', views.gallery_photo,
         name='gallery_photo'),
    # get a list of galleries of a specific user API
    path('user/<int:userpk>', views.user_galleries,
         name='user_galleries'),

]
