from project.permissions import check_permission
from gallery.serializers import CreateGallerySerializer
from accounts.views import verifying_user
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *
from django.urls import reverse
from rest_framework.views import status
from .functions import *
from accounts.views import *


# Create your tests here.
def create_test_user(email):
#prepare user
    first_name = 'test2'
    last_name = 'name'
    age = '50'
    password = 'Kamel1234567'
    email = email
    Account.objects.create_user(email,first_name,last_name,age,password)
    user=Account.objects.get(email = email)
    verifying_user(user)
    return user 
    
class TestModels(TestCase):
    def test_model_str(self):
        gallery_obj = Gallery.objects.create(title="New Gallery")
        comment_obj = Comments.objects.create(content="New comment")
        self.assertEqual(str(gallery_obj), "New Gallery")
        self.assertEqual(str(comment_obj), "New comment")

class GallerySerializerTests(TestCase):

    # def setUp(self):
    #     Gallery.objects.create(title='just a title', description='just a des')
    def test_create_gallery_success(self):
        # prepare gallery data
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = CreateGallerySerializer(data = data)
        serializer.is_valid()
        self.assertEqual(serializer.errors,{})

    def test_create_gallery_missing_title(self):
        # prepare gallery data
        data={}
        description='description'
        for variable in ["description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = CreateGallerySerializer(data = data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['title'][0],'This field is required.')

    def test_create_gallery_exceeds_title(self):
        # prepare gallery data
        data={}
        title=''
        for i in range (101):
            title=title + 's'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = CreateGallerySerializer(data = data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['title'][0],'Ensure this field has no more than 100 characters.')           

    def test_change_gallery_title(self):
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = CreateGallerySerializer(data = data)
        serializer.is_valid()
        serializer.save()
        obj=Gallery.objects.get(title=title)
        title='new'
        data={}
        title='new'
        for variable in ["title"]:
            data[variable] = eval(variable)
        changed_serializer= CreateGallerySerializer(obj,data=data) 
        changed_serializer.is_valid()
        changed_serializer.save()
        gallery_obj=Gallery.objects.get(title=title)
        self.assertEqual(gallery_obj.title,'new')

    def test_change_gallery_description(self):
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = CreateGallerySerializer(data = data)
        serializer.is_valid()
        serializer.save()
        obj=Gallery.objects.get(title=title)
        data={}
        title='title'
        description='new'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)
        changed_serializer= CreateGallerySerializer(obj,data=data) 
        changed_serializer.is_valid()
        changed_serializer.save()
        gallery_obj=Gallery.objects.get(title=title)
        self.assertEqual(gallery_obj.description,'new')

    def test_delete_gallery(self):
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = CreateGallerySerializer(data = data)
        serializer.is_valid()
        serializer.save()
        gallery_obj=Gallery.objects.get(title=title)
        gallery_obj.delete()   
        deleted_obj=Gallery.objects.filter(title=title)
        self.assertEqual(deleted_obj.exists(),False)


class GalleryFunctionsTests(TestCase):   
    def test_check_gallery_existence_success(self):
        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        gallery_obj=Gallery.objects.all().first()
        bool,response,_=check_gallery_exists(gallery_obj.id)
        self.assertEqual(response,'')
        self.assertEqual(bool,True)


    def test_check_photo_existence_success(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,
        photo_width=22,owner=user)
        photo_obj=Photo.objects.all().first()
        bool,response,_=check_photo_exists(photo_obj.id)
        self.assertEqual(response,'')
        self.assertEqual(bool,True)


    def test_check_comment_existence_success(self):
        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        gallery_obj=Gallery.objects.all().first()
        Comments.objects.create(content='content',owner=user,gallery=gallery_obj)
        comment_obj=Comments.objects.all().first()
        bool,response,_=check_comment_exists(comment_obj.id,gallery_obj)
        self.assertEqual(response,'')
        self.assertEqual(bool,True)

    def test_existence_of_object_in_list(self):
        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        gallery_obj=Gallery.objects.all().first()
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,
        photo_width=22,owner=user)
        photo_obj=Photo.objects.all().first()
        photo_obj.gallery_photos.add(gallery_obj)
        bool= check_existence_of_object_in_list(photo_obj,gallery_obj.photos.all())
        self.assertEqual(bool,True)
         
    def test_check_gallery_existence_failure(self):
        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        gallery_obj=Gallery.objects.all().first()
        gallery_obj.delete()
        bool,response,_=check_gallery_exists(gallery_obj.id)
        self.assertEqual(response,404)
        self.assertEqual(bool,False)

    def test_check_comment_existence_failure(self):
            user=create_test_user('test@gmail.com')
            Gallery.objects.create(title='title',description='description',owner=user)
            gallery_obj=Gallery.objects.all().first()
            Comments.objects.create(content='content',owner=user,gallery=gallery_obj)
            comment_obj=Comments.objects.all().first()
            comment_obj.delete()
            bool,response,_=check_comment_exists(comment_obj.id,gallery_obj)
            self.assertEqual(response,404)
            self.assertEqual(bool,False)

    def test_check_photo_existence_failure(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        photo_obj=Photo.objects.all().first()
        photo_obj.delete()
        bool,response,_=check_photo_exists(photo_obj.id)
        self.assertEqual(response,404)
        self.assertEqual(bool,False)
            
   
    def test_check_object_existence_in_list_failure(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        photo_obj=Photo.objects.all().first()
        Gallery.objects.create(title='title',description='description',owner=user)
        gallery_obj=Gallery.objects.all().first()
        bool= check_existence_of_object_in_list(photo_obj,gallery_obj.photos.all())
        self.assertEqual(bool, False)    

    def test_create_gallery_with_primary_photo_success(self):
        
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)

        photo_obj= Photo.objects.all().first()
        bool,response=check_permission(user,photo_obj) 
        self.assertEqual(bool,True)
        self.assertEqual(response,'')
        public_photo= check_photo_privacy(photo_obj)
        self.assertEqual(public_photo,True)
        title='title'
        description= 'description'
        owner = create_test_user('new@gmail.com')
        create_gallery_with_primary_photo(title ,description, owner, photo_obj.id ,photo_obj)
        gallery_obj=Gallery.objects.all().first()
        self.assertEqual(gallery_obj.title,'title')
        self.assertEqual(gallery_obj.primary_photo_id,photo_obj.id)
        self.assertEqual(gallery_obj.count_media,1)
        self.assertEqual(owner.galleries_count,1)

    def test_add_private_photo_to_gallery_failure(self):
        user=create_test_user('test2@gmail.com')
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=user,is_public=False)

        photo_obj= Photo.objects.all().first()
        bool,response=check_permission(user,photo_obj) 
        self.assertEqual(bool,True)
        self.assertEqual(response,'')
        public_photo= check_photo_privacy(photo_obj)
        self.assertEqual(public_photo,False)
        title='title2'
        description= 'description2'
        owner = create_test_user('new2@gmail.com')
        Gallery.objects.create(owner=owner, title=title,description=description)
        gallery_obj=Gallery.objects.all().first()
        response= add_photo_to_gallery(owner,photo_obj,gallery_obj,photo_obj.id)
        self.assertEqual(gallery_obj.title,'title2')
        self.assertEqual(response['privacy'][0],'photo must be public.')
        self.assertEqual(gallery_obj.primary_photo_id,None)

    def test_add_owner_photo_to_his_gallery_failure(self):
        user=create_test_user('test2@gmail.com')
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=user)

        photo_obj= Photo.objects.all().first()
        title='title2'
        description= 'description2'
        Gallery.objects.create(owner=user, title=title,description=description)

        gallery_obj=Gallery.objects.all().first()
        response= add_photo_to_gallery(user,photo_obj,gallery_obj,photo_obj.id)
        self.assertEqual(gallery_obj.title,'title2')
        self.assertEqual(gallery_obj.primary_photo_id,None)               
        self.assertEqual(response['photo_owner'][0],'Cant add your own photo.')

    def test_add_existed_photo_in_gallery_failure(self):
        owner=create_test_user('test@gmail.com')
        title='title2'
        description= 'description2'
        Gallery.objects.create(owner=owner, title=title,description=description,count_media=500)
        gallery_obj=Gallery.objects.all().first()
        self.assertEqual(gallery_obj.title,'title2')
        user=create_test_user('test2@gmail.com')
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=user)

        photo_obj= Photo.objects.all().first()
        response= add_photo_to_gallery(owner,photo_obj,gallery_obj,photo_obj.id)
        self.assertEqual(response['limit'][0],'max 500 photos in a gallery.')    
    
    
    def test_remove_photo_from_gallery_success(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)

        photo_obj= Photo.objects.all().first()
        title='title'
        description= 'description'
        owner = create_test_user('new@gmail.com')
        create_gallery_with_primary_photo(title ,description, owner, photo_obj.id ,photo_obj)
        gallery_obj=Gallery.objects.all().first()
        self.assertEqual(gallery_obj.title,'title')
        self.assertEqual(gallery_obj.primary_photo_id,photo_obj.id)
        self.assertEqual(gallery_obj.count_media,1)
        response= remove_photo_from_gallery(photo_obj,gallery_obj,user)
        self.assertEqual(gallery_obj.count_media,0)
        self.assertEqual(gallery_obj.primary_photo_id,None)               
        self.assertEqual(response,204)  


    def test_remove_photo_from_gallery_failure(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        photo_obj= Photo.objects.all().first()
        title='title'
        description= 'description'
        owner = create_test_user('new@gmail.com')
        create_gallery_with_primary_photo(title ,description, owner, photo_obj.id ,photo_obj)
        gallery_obj=Gallery.objects.all().first()
        remove_photo_from_gallery(photo_obj,gallery_obj,user)
        response= remove_photo_from_gallery(photo_obj,gallery_obj,user)
        self.assertEqual(response,400)               

    
    def test_search_gallery_with_title_found(self):
        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        bool,response,_=search_gallery('t')
        self.assertEqual(response,200)    
        self.assertEqual(bool,True)
    
    def test_search_gallery_with_title_no_found(self):
        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        bool,response,_=search_gallery('a')
        self.assertEqual(response,404)    
        self.assertEqual(bool,False)

    def test_get_user_galleries_succeded(self):

        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        owner=create_test_user('test2@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=owner)
        bool,response,list=get_user_galleries(1)
        self.assertEqual(response,200)    
        self.assertEqual(bool,True)

    def test_get_user_galleries_succeded(self):

        user=create_test_user('test@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=user)
        owner=create_test_user('test2@gmail.com')
        Gallery.objects.create(title='title',description='description',owner=owner)
        bool,response,list=get_user_galleries(2)
        self.assertEqual(response,404)    
        self.assertEqual(bool,False)
