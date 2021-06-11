from django.urls import path, include
from group import views
app_name = 'group'

urlpatterns = [
     # group
     # create group or get groups user is a member of APIs
     path('', views.group_get_create, name='group_get_create'),

     # join or leave group APIs
     path('<int:id>', views.join_leave_group, name='join_leave_group'),

     # get specific group APIs
     path('<int:id>/info', views.group_info, name='group_info'),

     # get public groups user is a member of APIs
     path('user/<int:id>', views.group_list, name='group_list'),

     # get member list of a group APIs
     path('<int:id>/members', views.member_list, name='member_list'),

     # search groups
     # user is a member of APIs
     # path('member/search', views.find_my_groups, name='find_my_groups'),

     # all groups APIs
     path('search', views.find_groups, name='find_groups'),

     # topics
     # create topic APIs
     path('<int:group_id>/topic', views.create_topic, name='create_topic'),

     # get list of topics in specific group APIs
     path('<int:group_id>/topic/list', views.topic_list, name='topic_list'),

     # get topic info in a specific group APIs
     path('<int:group_id>/topic/<int:topic_id>/info', views.topic_info,
          name='topic_info'),

     # edit or delete topic APIs
     # edit topic subject
     path('<int:group_id>/topic/<int:topic_id>', views.edit_delete_topic,
          name='edit_delete_topic'),

     # edit topic message
     path('<int:group_id>/topic/<int:topic_id>/message',
          views.edit_topic_message,
          name='edit_topic_message'),

     # search for a topic by its message API
     path('<int:group_id>/search', views.find_topic,  name='topic-search'),


     # replies
     # create reply APIs
     path('<int:group_id>/topic/<int:topic_id>/reply', views.create_reply,
          name='create_reply'),

     # get list of replies in specific topic APIs
     path('<int:group_id>/topic/<int:topic_id>/reply/list', views.reply_info,
          name='reply_info'),

     # get reply info in a specific topic APIs
     path('<int:group_id>/topic/<int:topic_id>/reply/<int:reply_id>/info',
          views.reply_info, name='reply_info'),

     # edit or delete reply APIs
     path('<int:group_id>/topic/<int:topic_id>/reply/<int:reply_id>',
          views.edit_delete_reply, name='edit_delete_reply'),


     # admin
     # edit group rules APIs
     path('<int:group_id>/admin/rules', views.edit_group_rules,
          name='edit_group_rules'),

     # edit group name and description APIs
     path('<int:group_id>/admin/name', views.edit_group_name,
          name='edit_group_name'),

     # edit group roles APIs
     path('<int:group_id>/admin/roles', views.edit_group_roles,
          name='edit_group_roles'),

     # edit group privacy APIs
     path('<int:group_id>/admin/privacy', views.edit_group_privacy,
          name='edit_group_privacy'),

     # edit group safety level APIs
     path('<int:group_id>/admin/18plus', views.edit_group_18plus,
          name='edit_group_18plus'),

     # promote or remove member APIs
     path('<int:group_id>/member/<int:member_id>', views.member_manage,
          name='member_manage'),


     # join group request
     # add or cancel join request group and get list of requests APIs
     path('<int:id>/request', views.group_join_request,
          name='group_join_request'),

     # accept or decline pending join request (by admin)
     path('<int:group_id>/request/<int:pending_id>',
          views.group_join_request_respond,
          name='group_join_request_respond'),


     # photos
     # get list of photos in a specific group API
     path('<int:group_id>/photos', views.group_photos,
          name='group_photos'),

     # add or remove a specific photo in a specific group APIs
     path('<int:group_id>/photos/<int:photo_id>', views.group_photo,
          name='group_photo'),

     # get list of groups a photo can added to API
     path('photos', views.group_photo_list,
          name='group_photo_list'),

     # accept or decline invite request notification to add photo to groups
     path('<int:group_id>/photos/<int:photo_id>/respond/<int:sender_id>',
          views.group_photo_request_respond,
          name='group_photo_request_respond'),
     
     # search for a photo in group by its title API
     path('<int:group_id>/search', views.find_topic,  name='topic-search'),

     # get top 5 contributers
     path('<int:group_id>/top', views.top_contributers,
          name='top_contributers'),

]
