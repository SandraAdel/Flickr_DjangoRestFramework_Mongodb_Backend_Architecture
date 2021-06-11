
from django.urls import path, include
from . import views
from . import api
app_name = 'photosets'
urlpatterns = [
    
    
    path('<int:id>', views.set_list),
    #   apis
    path('list', api.set_lists, name='set_lists'),
    #   getting the list of photosets of a given user:
    path('list/<int:id>', api.get_lists, name='get_lists'),
    #     adding a photoset by a user and setting its primary photo:
    path('create/<int:photo_id>', api.create_set, name='create_lists'),
    #     deleting a given photoset:
    path('delete/<int:id>', api.delete_set, name='delete_lists'),
    #     edit metadata of a given photoset:
    path('edit/<int:id>', api.edit_meta, name='edit_meta'),
    #   adding a comment to a given photoset:
    path('<int:id>/create-comment', api.create_comment,
         name='create_comment'),
     #   deleting a given comment:
    path('<int:set_id>/delete-comment/<int:comment_id>', api.delete_comment,
         name='delete_comment'),
     #    editing a given comment:
    path('<int:set_id>/edit-comment/<int:comment_id>', api.edit_comment,
     name='edit_comment'),
     #    get comments list on a given photoset:
    path('<int:id>/get-comments', api.get_comments_list, name='get_comment'),
    #     add and delete a given photo to a given photoset:
    path('<int:set_id>/<int:photo_id>/photo', api.photo, name='photo'),
    #     get photos in a given photoset:
    path('<int:set_id>/get-photo', api.get_photos, name='get_photo'),
    #     get information about a given photoset:
    path('<int:id>/get-info', api.get_information, name='get_information'),
    # get the photoset that a given photo belongs to:
    path('<int:photo_id>/get-set', api.photo_sets, name='get_sets'),
    # search for a photoset by its title:
    path('search', api.search, name='search'),
]