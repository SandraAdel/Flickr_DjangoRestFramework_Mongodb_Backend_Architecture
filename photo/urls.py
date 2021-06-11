from django.urls import path, include
from . import views

app_name = 'photo'

urlpatterns = [

   # Set or Get photo permissions APIs
    path('<int:id>/perms', views.set_or_get_perms, name='set_or_get_perms'),

    # Set photo meta API
    path('<int:id>/meta', views.set_meta, name='set_meta'),

    # Set photo dates API
    path('<int:id>/dates', views.set_dates, name='set_dates'),

    # Edit or delete photo comment APIs
    path('comments/<int:id>', views.edit_or_delete_comment,
         name='edit_or_delete_comment'),

    # Edit or delete photo note APIs
    path('notes/<int:id>', views.edit_or_delete_note,
         name='edit_or_delete_note'),

    # Delete photo or get photo info API
    path('<int:id>', views.delete_photo_or_get_photo_info, name='delete_photo_or_get_photo_info'),

    # Add a photo note or get photo notes APIs
    path('<int:id>/notes', views.add_note_or_get_photo_notes, name='add_note_or_get_photo_notes'),

    # Add a photo comment or get photo comments APIs
    path('<int:id>/comments', views.add_comment_or_get_photo_comments, name='add_comment_or_get_photo_comments'),

    # Add or get photo tags APIs
    path('<int:id>/tags', views.add_or_get_tags, name='add_or_get_tags'),

    # Remove photo tag API
    path('tags/<int:id>', views.remove_tag, name='remove_tag'),

    # Tag or untag person in photo API
    path('<int:photo_id>/people/<int:person_id>', views.tag_or_untag_person, name='tag_or_untag_person'),

    # Get people tag in photo API
    path('<int:id>/people', views.get_people_tagged, name='get_people_tagged'),

    # Get recent photos API
    path('recent', views.get_recent_photos, name='get_recent_photos'),

    # Photo search API
    path('search', views.search_photos, name='search_photos'),

    # Rotate photo API
    path('<int:id>/transform/rotate', views.rotate_photo, name='rotate_photo'),

    
    # Faves
    # get the favourites photos list API
    path('faves', views.faves_list, name='faves_list'),

    # get List of the users who faved a photo API
    path('<int:id>/faves', views.photo_faves, name='photo_faves'),

    # add or remove a specific photo to the favourites photos API
    path('<int:id>/fav', views.fav_photo, name='fav_photo'),
    
    # Upload
    path('upload', views.upload_media, name='upload_media'),

     # Get public photos of a given user:
    path('<int:id>/public', views.get_public, name='get_public'),

     #  Get public photos of loggedin user:
     path('publiclogged', views.get_public_logged, name='get_publiclogged'),

     #  Get all photos of loggedin user:
     path('photoslogged', views.get_photos_logged, name='get_photoslogged'),
     
     #Home API
     path('home', views.Home, name='Home'),

]


