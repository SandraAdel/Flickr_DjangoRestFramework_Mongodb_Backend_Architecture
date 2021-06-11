from .models import *
from .models import commentss
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404, response
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from django import forms
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from project.permissions import IsOwner
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from photo.models import *
from photo.serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class RespondPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1

def set_primary(serializer, photo_id, get_photo,sets_obj):
    """
    Set primary photo of a given photoset
    
    :param name: serializer
    :param type: object
    :param name: photo_id : Photo to set photoset with
    :param type: int
    :param name: get_photo 
    :param type: gallery object
    :param name: sets : sets to add the photo to
    :param type: sets object
    :param name: phopk : photo's primary key 
    :param type: int
    :return: None
    """
    serializer.save(primary=photo_id)         # to set the primary photo of a given photoset
    get_photo.sets_photos.add(sets_obj)

def photos (photo_id):   # to get a photo from the database
    
    """
    Get a photo from the database

    :param name: photo_id 
    :param type: int
    :return name: get_photo 
    :return type: photo object
    :return name: bool
    """
    bool = True #to check the existance of a given set
    try:
        get_photo = Photo.objects.get(id=photo_id)
        response=status.HTTP_200_OK
        return get_photo, response, bool
        
    except ObjectDoesNotExist:
        get_photo=None
        response=status.HTTP_404_NOT_FOUND
        bool = False
        return get_photo, response, bool
        
def add_photo(get_photo,get_list):
    """
    Add a photo to the photosets
    
    :param name: get_photo 
    :param type: object
    :param name: get_list 
    :param type: object
    :returns: None
    """
    get_photo.sets_photos.add(get_list)

def delete_photo(get_list, deleted_photo):
    """
    delete a photo to the photosets
    
    :param type: object
    :param name: deleted_photo 
    :param name: get_list 
    :param type: object
    :returns: None
    """
    get_list.photos.remove(deleted_photo)

def search_set(value):
    """
    search set by photo title
    
    :param name: value 
    :param type: int 
    :param name: get_list 
    :param type: object
    :return name: bool 
    :return type: object
    :return name: get_list 
    :return type: object
    """
    response=''
    bool= False
    set = sets.objects.filter(title__icontains=value)\
    .order_by('-date_create')
    if set:
        bool= True
    else:
       response = status.HTTP_404_NOT_FOUND
    return bool, response, set
        
    
def check_set(id):
    """
    check existing of a specific set
    
    :param name: get_list 
    :param type: object
    :param name: bool 
    :param type: object
    :param name: get_list 
    :param type: object
    """
    bool = True #to check the existance of a given set
    try:
        get_list = sets.objects.get(id=id)
        response=status.HTTP_200_OK
        return get_list, response, bool
        
    except ObjectDoesNotExist:
        get_list=None
        response=status.HTTP_404_NOT_FOUND
        bool = False
        return get_list, response, bool

def check_comm(get_list, comment_id):
    """
    check the existance of a given comment
        
    :param name: get_list 
    :param type: object
    :param name: comment_id 
    :param type: int
    :return name: bool 
    :return type: object
    :return name: get_comment 
    :return type: object
    :return name: Response 
    :return type: str
    """
    bool = True #to check the existance of a given comment
    try:
       
        get_comment=get_list.comment.get(id=comment_id)  
        response=status.HTTP_200_OK
        return get_comment, response, bool
        
    except :
        get_comment=None
        response=status.HTTP_404_NOT_FOUND
        bool = False
        return get_comment, response, bool

def check_user(get_list, request):
    """
    check user
        
    :param name: get_list 
    :param type: object
    :param name: user 
    :param type: object
    :return name: status 
    :return type: str
    :return name: Response 
    :return type: str
    """
    Response=''
    statuss=''
    if (get_list.owner != request.user):
        Response=(
                {'stat': 'fail',
                'message': 'User does not have permission '})
           
        statuss=status.HTTP_403_FORBIDDEN
    return Response, statuss

def exist_photo(get_list, get_photo):
    """
    check whether the photo exists in the set
            
    :param name: get_list 
    :param type: object
    :param name: get_photo 
    :param type: object
    :return name: status 
    :return type: str
    :return name: Response 
    :return type: str
    """
    Response=''
    statuss=''
    photoos= get_list.photos.all()
    if get_photo in photoos: #check whether the photo exists in the set 
        Response=(
                {'stat': 'fail',
                'message': 'photo already exists'})
        statuss=status.HTTP_403_FORBIDDEN
    return Response, statuss

def photo_exists(get_list, photo_id):
    """
    Check if photo exists in a set
        
    :param name: get_list 
    :param type: object
    :param name: photo_id 
    :param type: int
    :param name: deleted_photo 
    :param type: object
    :return name: status 
    :return type: str
    :return name: Response 
    :return type: str
    """
    Response=''
    statuss=''
    try:
        deleted_photo=get_list.photos.get(id=photo_id)
        return deleted_photo ,Response, statuss
    except ObjectDoesNotExist: #check whether the photo exists in the set 
        Response=(
                {'stat': 'fail',
                'message': 'photo does not exist'})
        statuss=status.HTTP_403_FORBIDDEN
        deleted_photo=None
        return deleted_photo ,Response, statuss


def comm_increment(serializer, get_list, request ): 
    # incrementing the comment count
    # when creating a new comment to a given set
    """
    Increment the comment count when creating a new comment to a given set
        
    :param name: serializer 
    :param type: object
    :param name: get_ist 
    :param type: object
    :param name: user 
    :param type: object
    :returns: None
    """
    serializer.save(sets=get_list, owner=request.user)
    get_list.count_comments += 1
    get_list.save()

def comm_decrement(get_list):
    """
    decrement comment count when creating a new comment to a given set
        
    :param name: get_ist 
    :param type: object
    :returns: None
    """
    get_list.count_comments -= 1
    get_list.save()  

def photo_increment(get_list):
    """
    increment photo 
        
    :param name: get_ist 
    :param type: object
    :returns: None
    """
    get_list.count_photos += 1
    get_list.save()

def photo_decrement(get_list):
    """
    decrement photo number
        
    :param name: get_ist 
    :param type: object
    :returns: None
    """
    get_list.count_photos -= 1    
    get_list.save()           

def sets_increment(request):
    """
    increment sets number 
        
    :param name: user 
    :param type: object
    :returns: None
    """
    user=request.user
    user.photosets_count +=1
    user.save()
   
def sets_decrement(request):
    """
    decrement photo number
        
    :param name: user 
    :param type: object
    :returns: None
    """
    user=request.user
    user.photosets_count -=1
    user.save()

@api_view(['GET'])
def set_lists(request):
    try:
   
        all_sets = sets.objects.all()
    except ObjectDoesNotExist:
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    photosets = sets_serializer(all_sets, many=True).data 
    return Response({'photosets': photosets})

@api_view(['GET'])
#   getting the list of photosets of a given user
def get_lists(request, id):
    try:

        get_list = sets.objects.all().filter(owner_id=id).order_by('-date_create')
        
    except ObjectDoesNotExist:
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    #  for pagination
    Paginator = RespondPagination()
    results = Paginator.paginate_queryset(get_list, request)
    photosets = sets_serializer(results, many=True).data
    return Paginator.get_paginated_response({'photosets': photosets})


@api_view(['GET'])  
#     get information about a given photoset
def get_information(request, id):
    get_list, response, bool = check_set(id)
    if bool:
        set = sets_serializer(get_list).data
        return Response({'photoset': set}, status=response)
    else:
        return Response(status=response)
    
    

@swagger_auto_schema( methods = ['POST'] , request_body = sets_serializer_post_swagger )
@api_view(['POST'])   
@permission_classes((IsAuthenticated,))
#adding a photoset by a user and setting its primary photo
def create_set(request, photo_id):
    get_photo, responses, boool = photos(photo_id)
    if boool:
            try:
        
                sets_obj=sets.objects.create(title=request.data['title'],
                                        owner=request.user)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = sets_serializer_post(sets_obj, data=request.data)
            
            if serializer.is_valid():
                set_primary(serializer, photo_id, get_photo,sets_obj)
                sets_increment(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(status=responses)
    
    
        
    

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
# deleting a given photoset
def delete_set(request, id):
    get_list, response, bool = check_set(id)
    if bool:
        
        responsee, statuss=check_user(get_list, request)
        if responsee!='':
            return Response(responsee, status=statuss)
        get_list.delete()
        
        sets_decrement(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=response)
    
        
@swagger_auto_schema( methods = ['PUT'] , request_body = sets_serializer_post_swagger )
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
#     edit metadata of a given photoset
def edit_meta(request, id):
    get_list, response, bool = check_set(id)
    if bool:
        
        responsee, statuss=check_user(get_list, request)
        if responsee!='':
            return Response(responsee, status=statuss)   
        
        serializer = sets_serializer_post(get_list, data=request.data)
        if serializer.is_valid():
            
            serializer.save()
        
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=response)



        
    
    
@swagger_auto_schema( methods = ['POST'] , request_body = comments_serializer_post )
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
#   adding a comment to a given photoset
def create_comment(request, id):
     # getting the photoset from database
    get_list, response, bool = check_set(id)
    if bool:
        
        responsee, statuss=check_user(get_list, request)
        if responsee!='':
            return Response(responsee, status=statuss)# check for the user
    
        serializer = comments_serializer_post(data=request.data)
        if serializer.is_valid():
            comm_increment(serializer, get_list, request )
            return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=response)
   

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
#   deleting a given comment
def delete_comment(request, comment_id, set_id):
    # getting the photoset from database
    get_list, response, bool = check_set(set_id)
    if bool:
        responsee, statuss=check_user(get_list, request)
        if responsee!='':
            return Response(responsee, status=statuss)# check for the user
    get_comment, responses, boool= check_comm(get_list, comment_id)
    if boool:
        get_comment.delete()
        comm_decrement(get_list)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=responses)


@swagger_auto_schema( methods = ['PUT'] , request_body = comments_serializer_post )
@api_view(['PUT'])
#    editing a given comment
@permission_classes((IsAuthenticated,))
def edit_comment(request, set_id, comment_id):
    # getting the photoset from database
    get_list, response, bool = check_set(set_id)
    if bool:
        responsee, statuss=check_user(get_list, request)
        if responsee!='':
            return Response(responsee, status=statuss)# check for the user
    get_comment, responses, boool= check_comm(get_list, comment_id)
    if boool:
        serializer = comments_serializer_post(get_comment, data=request.data)            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=responses)
    

@api_view(['GET'])
#    get comments list on a given photoset
def get_comments_list(request,id):
    get_list, response, bool = check_set(id)
    if bool:    
        set_list = get_list.comment.all() # getting all the comments from database
    
        comments = comments_serializer(set_list, many=True).data
        return Response({'comments': comments}, status=status.HTTP_200_OK)  
    else:
        return Response(status=response)


@api_view(['POST','DELETE'])  
#     add and delete a given photo to a given photoset
@permission_classes((IsAuthenticated,))
def photo(request, set_id, photo_id):
    get_list, response, bool = check_set(set_id)
    if bool:
        responsee, statuss=check_user(get_list, request)
        if responsee!='':
            return Response(responsee, status=statuss)# check for the user  
    else:
        return Response(status=response)
    if request.method == 'POST':
        get_photo, responses, boool = photos(photo_id)
        if boool:
            res, stat= exist_photo(get_list, get_photo)
            if res !='':
                return Response(res, status=stat) 
            else:
                get_photo.sets_photos.add(get_list)
                photo_increment(get_list)
                return Response( status=status.HTTP_200_OK)
        else:
            return Response(status=responses)
    if request.method == 'DELETE':
        deleted_photo ,Responser, statuss=photo_exists(get_list, photo_id)
        if Responser !='':
            return Response(Responser, status=statuss) 
        get_list.photos.remove(deleted_photo)
        photo_decrement(get_list)
        return Response( status=status.HTTP_200_OK)
        

@api_view(['GET'])  
#     get photos in a given photoset
def get_photos(request, set_id):
    try:
        get_list = sets.objects.get(id=set_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)      
    set_list = get_list.photos.all().order_by('-date_posted')
    photos = PhotoMetaSerializer(set_list, many=True).data
    if photos == []:
        return Response({'stat': 'fail',
                    'message': 'no photos'},status=status.HTTP_400_BAD_REQUEST)
      
    return Response({'photos': photos}, status=status.HTTP_200_OK)

@api_view(['GET'])
def photo_sets(request, photo_id):
#     get the photosets that a given photo belongs to
    try:
        photo_obj = Photo.objects.get(id=photo_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    sets = photo_obj.sets_photos.all()
    serializer = sets_serializer(sets, many=True)
    return Response(serializer.data)

test_param = openapi.Parameter('title', openapi.IN_QUERY, description="Search for set with title", type=openapi.TYPE_STRING)
user_response = openapi.Response('response description', sets_serializer)

@swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response})
@api_view(['GET'])
def search(request):
# search for a set by its title ordered from the oldest
    try:
        value = request.query_params.get("title")
        Sets = sets.objects.filter(title__icontains=value)\
            .order_by('-date_create')
    except:
        Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = sets_serializer(Sets, many=True)
    return Response(serializer.data)
