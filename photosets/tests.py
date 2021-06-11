from django.test import TestCase
from .serializer import sets_serializer
from .serializer import comments_serializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.shortcuts import render
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from . import urls
from .api import *
from project.permissions import check_permission
from accounts.views import verifying_user
from .models import *


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
    def test_model(self):
    
        set_obj = sets.objects.create(title="New set")
        self.assertEqual(str(set_obj), "New set")
        
  
    def test_objects_existence(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        photo_obj=Photo.objects.all().first()

        sets.objects.create(title='title',description='description',owner=user)
        set_obj=sets.objects.all().first()
        commentss.objects.create(contents='content',owner=user,sets=set_obj)
        comment_obj=commentss.objects.all().first()
        _, response, bool = check_set(set_obj.id)
        _, response1, bool1=check_comm(set_obj,comment_obj.id)
        _, response2, bool2=photos(photo_obj.id)
        self.assertEqual(response,200)
        self.assertEqual(bool, True)
        self.assertEqual(response1,200)
        self.assertEqual(bool1, True)
        self.assertEqual(response2,200)
        self.assertEqual(bool2, True)
        
    def test_objects_failure(self):
        user=create_test_user('test@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        photo_obj=Photo.objects.all().first()

        sets.objects.create(title='title',description='description',owner=user)
        set_obj=sets.objects.all().first()
        commentss.objects.create(contents='content',owner=user,sets=set_obj)
        comment_obj=commentss.objects.all().first()
        set_obj.delete()
        photo_obj.delete()
        comment_obj.delete()
        _, response, bool = check_set(set_obj.id)
        _, response1, bool1=check_comm(set_obj,comment_obj.id)
        _, response2, bool2=photos(photo_obj.id)
        self.assertEqual(response,404)
        self.assertEqual(bool, False)
        self.assertEqual(response1,404)
        self.assertEqual(bool1, False)
        self.assertEqual(response2,404)
        self.assertEqual(bool2, False)



    def test_set_creation(self):
        # prepare set data
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = sets_serializer_post(data = data)
        serializer.is_valid()
        self.assertEqual(serializer.errors,{})

    def test_create_set_missing_title(self):
        # prepare set data
        data={}
        description='description'
        for variable in ["description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = sets_serializer_post(data = data)
        serializer.is_valid()
        self.assertEqual(serializer.errors['title'][0],'This field is required.')

    def test_change_set_title(self):
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = sets_serializer_post(data = data)
        serializer.is_valid()
        serializer.save()
        obj=sets.objects.get(title=title)
        title='new'
        data={}
        title='new'
        for variable in ["title"]:
            data[variable] = eval(variable)
        changed_serializer= sets_serializer_post(obj,data=data) 
        changed_serializer.is_valid()
        changed_serializer.save()
        set_obj=sets.objects.get(title=title)
        self.assertEqual(set_obj.title,'new')


    def test_change_set_description(self):
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = sets_serializer_post(data = data)
        serializer.is_valid()
        serializer.save()
        obj=sets.objects.get(title=title)
        data={}
        title='title'
        description='new'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)
        changed_serializer= sets_serializer_post(obj,data=data) 
        changed_serializer.is_valid()
        changed_serializer.save()
        set_obj=sets.objects.get(title=title)
        self.assertEqual(set_obj.description,'new')

    def test_delete_set(self):
        data={}
        title='title'
        description='description'
        for variable in ["title", "description"]:
            data[variable] = eval(variable)

        #Sending data to serializer to test serializer
        serializer = sets_serializer_post(data = data)
        serializer.is_valid()
        serializer.save()
        set_obj=sets.objects.get(title=title)
        set_obj.delete()   
        deleted_obj=sets.objects.filter(title=title)
        self.assertEqual(deleted_obj.exists(),False)




    def test_add_existed_photo_in_set_failure(self):
        owner=create_test_user('test@gmail.com') # trying to add an existing photo
        title='title2'
        description= 'description2'
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=owner)
        photo_obj= Photo.objects.all().first()
        sets.objects.create(owner=owner, title=title,description=description)
        set_obj=sets.objects.all().first()
        self.assertEqual(set_obj.title,'title2')
        add_photo(photo_obj,set_obj)
        response, statuss= exist_photo(set_obj, photo_obj)
        self.assertEqual(statuss,403)  
        self.assertEqual(response['stat'],'fail')


    def test_delete_existed_photo_in_set_success(self):
        owner=create_test_user('test@gmail.com') # deleting an existing photo
        title='title2'
        description= 'description2'
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=owner)
        photo_obj= Photo.objects.all().first()
        sets.objects.create(owner=owner, title=title,description=description)
        set_obj=sets.objects.all().first()
        self.assertEqual(set_obj.title,'title2')
        add_photo(photo_obj,set_obj)
        delete_photo(set_obj, photo_obj)
        response, statuss= exist_photo(set_obj, photo_obj)
        self.assertEqual(statuss,'')  
        self.assertEqual(response,'')


    def test_delete_existed_photo_in_set_failure(self):
        owner=create_test_user('test@gmail.com') # trying to delete non existing photo in a set
        title='title2'
        description= 'description2'
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=owner)
        photo_obj= Photo.objects.all().first()
        Photo.objects.create(
            media_file='api/media/123.png',photo_height=123,photo_width=22,
            owner=owner)
        photo_obj2= Photo.objects.all().last()
        sets.objects.create(owner=owner, title=title,description=description)
        set_obj=sets.objects.all().first()
        self.assertEqual(set_obj.title,'title2')
        add_photo(photo_obj,set_obj)
        delete_photo(set_obj, photo_obj2)
        response, statuss= exist_photo(set_obj, photo_obj)
        self.assertEqual(statuss,403)  
        self.assertEqual(response['stat'],'fail')
        
    def test_search_set_with_title_found(self):
        user=create_test_user('test@gmail.com')
        sets.objects.create(title='title',description='description',owner=user)
        bool,response,_=search_set('t')
        self.assertEqual(response,'')    
        self.assertEqual(bool,True)      


    def test_search_set_with_title_no_found(self):
        user=create_test_user('test@gmail.com')
        sets.objects.create(title='title',description='description',owner=user)
        bool,response,_=search_set('a')
        self.assertEqual(response,404)    
        self.assertEqual(bool,False)

    