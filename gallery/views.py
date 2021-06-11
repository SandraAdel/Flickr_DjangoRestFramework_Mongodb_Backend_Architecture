from django.core import paginator
from django.db.models import fields
from django.http import response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from photo.models import *
from accounts.models import *
from .serializers import *
from photo.serializers import *
from project.permissions import check_permission
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from .functions import *



@api_view(['GET'])
def gallery_info(request, galpk):
    # get , edit and delete a specific gallery by its id
    exists, response, gallery_obj = check_gallery_exists(galpk)
    if not exists:
        return Response(status=response)
    #   GET
    serializer = GallerySerializer(gallery_obj)
    return Response(serializer.data)

@swagger_auto_schema( methods = ['PUT'] , request_body = CreateGallerySerializer )

@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def edit_or_delete_gallery(request, galpk): 

    exists, response, gallery_obj = check_gallery_exists(galpk)
    if not exists:
        return Response(status=response)     
    #   PUT
    if request.method == 'PUT':
        bool,response=check_permission(request.user,gallery_obj)        
        if not bool :
            return Response(status=response)
        serializer = CreateGallerySerializer(gallery_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #   DELETE
    elif request.method == 'DELETE':
        bool,response=check_permission(request.user,gallery_obj)        
        if not bool :
            return Response(status=response)
        gallery_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_galleries(request, userpk):
    # get a list of galleries of a specific user given its id
    Paginator = PageNumberPagination()
    Paginator.page_size = 20
    exists, response, gallery_list = get_user_galleries(userpk)
    if not exists:
        return Response(status=response)
    #   GET
    results = Paginator.paginate_queryset(gallery_list, request)
    galleries = GallerySerializer(results, many=True)
    return Paginator.get_paginated_response(
        galleries.data)


@swagger_auto_schema( methods = ['post'] , request_body = CreateGallerySerializer )

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def gallery_list(request):
    # get list of galleries or create a new one
    Paginator = PageNumberPagination()
    Paginator.page_size = 20
    # GET
    if request.method == 'GET':
        gallery_list = Gallery.objects.all()
        results = Paginator.paginate_queryset(gallery_list, request)
        galleries = GallerySerializer(results, many=True)
        return Paginator.get_paginated_response(
            galleries.data)
    # POST
    elif request.method == 'POST':
        serializer = CreateGallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            # increment the count of galleries in the profile of the user by 1
            increment_profile_items(request.user,'galleries_count')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

test_param = openapi.Parameter('title', openapi.IN_QUERY, description="Search for a gallery with title", type=openapi.TYPE_STRING)
user_response = openapi.Response('response description', GallerySerializer)

@swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def find_gallery(request):
    # search for a gallery by its title ordered from the oldest
    value = request.query_params.get("title")
    exists, response, galleries= search_gallery(value)
    if not exists:
        return Response(status=response)
    serializer = GallerySerializer(galleries, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def gallery_comments_list(request, galpk):
    # get list of comments or create a new one
    #  to a specific gallery given its id
    exists, response, gallery_obj = check_gallery_exists(galpk)
    if not exists:
        return Response(status=response)
    # GET
    comments = gallery_obj.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@swagger_auto_schema( methods = ['POST'] , request_body = CreateCommentSerializer )
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_gallery_comment(request, galpk):
    # get list of comments or create a new one
    #  to a specific gallery given its id
    exists, response, gallery_obj = check_gallery_exists(galpk)
    if not exists:
        return Response(status=response)
    # POST
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            gallery=gallery_obj, owner=request.user)
        # increment the count of comments in that gallery by 1
        increment_gallery_items(gallery_obj, 'count_comments')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema( methods = ['PUT'] , request_body = CreateCommentSerializer )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def gallery_comment(request, galpk, compk):
    # get ,edit and delete a specific comment on a gallery given their ids

    gallery_exists, gallery_response, gallery_obj = check_gallery_exists(galpk)
    if not gallery_exists:
        return Response(gallery_response)
    comment_exists, comment_response, comment_obj = check_comment_exists(compk,gallery_obj)
    if not comment_exists:
        return Response(comment_response)
    # GET
    if request.method == 'GET':
        serializer = CommentSerializer(comment_obj)
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        bool, response=check_permission(request.user ,comment_obj)        
        if not bool:
            return Response(status=response)
        serializer = CommentSerializer(comment_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #   DELETE
    elif request.method == 'DELETE':
        bool, response=check_permission(request.user ,comment_obj)        
        if not bool:
            return Response(status=response)
        comment_obj.delete()
        # decrement the count of comments in that gallery by 1
        decrement_gallery_items(comment_obj,'count_comments')
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def gallery_photos(request, galpk):
    # get the photos list in a specific gallery given the gallery id
    exists, response, gallery_obj = check_gallery_exists(galpk)
    if not exists:
        return Response(status=response)
    # GET
    if request.method == 'GET':
        photos = gallery_obj.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def photo_galleries(request, phopk):
    # get the list of galleries in which
    # a specific photo is added given the photo id
    exists, response, photo_obj = check_photo_exists(phopk)
    if not exists:
        return Response(status=response)
    # GET
    if request.method == 'GET':
        galleries = photo_obj.gallery_photos.all()
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data)

@swagger_auto_schema( methods = ['POST'] , request_body = CreateGallerySerializer )

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_gallery_with_primary_photo(request, phopk):
    # get the list of galleries in which
    # a specific photo is added given the photo id
    exists, response, photo_obj = check_photo_exists(phopk)
    if not exists:
        return Response(status=response)
    # POST    
    # create gallery with primary photo
    bool,response=check_permission(request.user,photo_obj)  
    public_photo= check_photo_privacy(photo_obj)
    if not bool and public_photo :
        title=request.data['title']
        description= request.data['description']
        
        # create_gallery_with_primary_photo(title,description, request.user, phopk ,photo_obj)
        gallery_obj = Gallery.objects.create( title= title,
        description=description, owner=request.user)
        set_primary_photo_id(gallery_obj,phopk)
        photo_obj.gallery_photos.add(gallery_obj)
        # increment the count of items in that gallery by 1
        increment_gallery_items(gallery_obj,'count_media')
        # increment the count of galleries in the profile of the user by 1
        increment_profile_items(request.user,'galleries_count')
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def gallery_photo(request, galpk, phopk):
    # add or remove a specific photo in a specific gallery given their ids
    gallery_exists, response, gallery_obj = check_gallery_exists(galpk)
    if not gallery_exists:
        return Response(status=response)
    photo_exists, photo_response, photo_obj = check_photo_exists(phopk)
    if not photo_exists:
        return Response(status=photo_response)
    bool,response=check_permission(request.user,gallery_obj)        
    if not bool :
        return Response(status=response)
    # put a flag to see whether the photo is already in the gallery or not
    if request.method == 'POST':
        response = add_photo_to_gallery(request.user,photo_obj,gallery_obj,phopk)
        # send_gallery_notification(photo_obj, request.user, gallery_obj)
        return Response(status=response)
    #   DELETE
    elif request.method == 'DELETE':
        response= remove_photo_from_gallery(photo_obj,gallery_obj,request.user) 
    return Response(status=response)
