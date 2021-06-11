from .models import *
from accounts.models import *
import os
from accounts.views import *
from rest_framework import status
from django.conf import settings              



def search_in_search_place(photo_ids_list, user):
    """
    Search in search place
    
    :param name: photo_ids_list 
    :param type: object
    :param name: user 
    :param type: object
    :param name: user : user performing followed
    :param type: object
    :return name: user_required_photos
    :return type: object
    :return name: following_required_photos
    :return type: object
    :return name: everyone_required_photos
    :return type: object
    """    
    
    following_list_ids = []
    following_list = user.follow_follower.all()
    for following in following_list:
        following_list_ids.append(following.id)

    # User's photos
    user_required_photos = Photo.objects.filter(is_public=True, owner_id=user.id, id__in=photo_ids_list).order_by('-date_posted')

    # Following's photos
    following_required_photos = Photo.objects.filter(is_public=True, owner_id__in=following_list_ids, id__in=photo_ids_list).order_by('-date_posted')
    
    # Everyone's photos
    following_list_ids.append(user.id)
    ids_list = following_list_ids
    everyone_required_photos = Photo.objects.filter(is_public=True, id__in=photo_ids_list).exclude(owner_id__in=ids_list).order_by('-date_posted')

    # return all
    return user_required_photos, following_required_photos, everyone_required_photos


def search_according_to_all_or_tags(request_data):
    """
    Search according to all or tags
    
    :param name: data 
    :param type: string
    :return name: photo_ids_list
    :return type: object
    """  
    
    # Searching for search_text in title, description & tags OR tags only
    list = request_data.get('search_text').split()
    photo_ids_list = []

    # If all_or_tags is not provided or is set to (all),
    # search for search_text in title, description & tags
    if ('all_or_tags' not in request_data) or (request_data.get('all_or_tags') == 'all'):

        for text in list:
            photos = Photo.objects.filter(title__icontains=text) | Photo.objects.filter(description__icontains=text)
            for photo in photos:
                photo_ids_list.append(photo.id)
            tags = Tag.objects.filter(tag_text__icontains=text)
            for tag in tags:
                photo_ids_list.append(tag.photo_id)  

        return  photo_ids_list

   # If all_or_tags is set to (tags),
   # search for search_text in tags ONLY
    elif (request_data.get('all_or_tags') == 'tags'):

        for text in list:
            tags = Tag.objects.filter(tag_text__icontains=text)
            for tag in tags:
                photo_ids_list.append(tag.photo_id)
        
        return  photo_ids_list

    else:
        return None

def limit_photos_number(photos, max_limit):
    """
        Limit photo number
        
        :param name: photos 
        :param type: object
        :param name: max_limit 
        :param type: int
        
        :return name: required_photos
        :return type: object
        """   

    required_photos_ids_list = []
    count = 1
    for photo in photos:
        if count <= max_limit:
            required_photos_ids_list.append(photo.id)
            count += 1

    required_photos = Photo.objects.filter(id__in=required_photos_ids_list).order_by('-date_posted')
    return required_photos


def get_search_photos_anonymous_case():
    """
     get search photos anonymous case

    Returns:
        :return: user_required_photos
        :return: following_required_photos
        :return: everyone_required_photos
    """
    
    user_required_photos = []
    following_required_photos = []
    everyone_required_photos = Photo.objects.filter(is_public=True).order_by('-date_posted')
    everyone_required_photos = limit_photos_number(everyone_required_photos, 300)
    return user_required_photos, following_required_photos, everyone_required_photos


def filter_by_date(is_user_anonymous, date_type, min_date, max_date, user_required_photos, following_required_photos, everyone_required_photos):
    """
    Filter by date
    :param name: is_user_anonymous 
    :param type: bool
    :param name: date_type 
    :param type: str
    :param name: min_date 
    :param type: str
    :param name: max_date 
    :param type: str
    :param name: user_required_photos 
    :param type: object
    :param name: following_required_photos 
    :param type: object
    :param name: everyone_required_photos 
    :param type: object

    :return: user_required_photos
    :return: following_required_photos
    :return: everyone_required_photos
    """
    if date_type == 'upload_date':

        if is_user_anonymous:
            everyone_required_photos = everyone_required_photos.filter(date_posted__range=(min_date, max_date))
        else:
            user_required_photos = user_required_photos.filter(date_posted__range=(min_date, max_date))
            following_required_photos = following_required_photos.filter(date_posted__range=(min_date, max_date))
            everyone_required_photos = everyone_required_photos.filter(date_posted__range=(min_date, max_date))

    elif date_type == 'taken_date':

        if is_user_anonymous:
                everyone_required_photos = everyone_required_photos.filter(date_taken__range=(min_date, max_date))
        else:
            user_required_photos = user_required_photos.filter(date_taken__range=(min_date, max_date))
            following_required_photos = following_required_photos.filter(date_taken__range=(min_date, max_date))
            everyone_required_photos = everyone_required_photos.filter(date_taken__range=(min_date, max_date))

    return user_required_photos, following_required_photos, everyone_required_photos


def get_required_photo(id):
    """Get required photo

        :param name: id 
        :param type: int
        
    
        :return: required_photo
        :return: photo_id
        :return: photo
    """

    required_photo = Photo.objects.get(id=id)
    return required_photo


def get_required_comment_and_its_photo(id):
    """Get required comment and photo

            :param name: id 
            :param type: int
            
        
            :return: required_comment
            :return: photo_id
            :return: photo
        """

    required_comment = Comment.objects.get(comment_id=id)
    photo_id = required_comment.photo_id
    photo = Photo.objects.get(id=photo_id)
    return required_comment, photo_id, photo


def get_required_note_and_its_photo(id):
    """
    Get required note and photo

        :param name: id 
        :param type: int
        
    
        :return: required_note
        :return: photo_id
        :return: photo
    """

    required_note = Note.objects.get(note_id=id)
    photo_id = required_note.photo_id
    photo = Photo.objects.get(id=photo_id)
    return required_note, photo_id, photo


def get_required_tag_and_its_photo(id):
    """
    Get required tag and photo

        :param name: id 
        :param type: int
        
    
        :return: required_tag
        :return: photo
    """

    required_tag = Tag.objects.get(tag_id=id)
    photo_id = required_tag .photo_id
    photo = Photo.objects.get(id=photo_id)
    return required_tag, photo


def get_photo_and_person_tagged(photo_id, person_id):
    """
        Get required photo and person tagged

        :param name: photo_id 
        :param type: int
        :param name: person_id 
        :param type: int
        
    
        :return: photo
        :return: person_tagged
    """

    photo = Photo.objects.get(id=photo_id)
    person_tagged = Account.objects.get(id=person_id)
    return photo, person_tagged


def get_note_coordinates(request_data):
    """
        Get note coordinate

        :param name: data 
        :param type: str
        :param name: person_id 
        :param type: int
        
    
        :return: left_coord
        :return: top_coord
        :return: note_width
        :return: note_height
    """
    left_coord = request_data['left_coord']
    top_coord = request_data['top_coord']
    note_width = request_data['note_width']
    note_height = request_data['note_height']
    return left_coord, top_coord, note_width, note_height


def remove_photo_path_locally(photo):
    """
        Remove photo path locally

        :param name: photo 
        :param type: object
        
    
        :returns: None
    """

    media_file = photo.media_file
    os.remove('media/' + str(media_file))


def get_photo_permission(photo, perm):
    """
        get photo permission

        :param name: photo 
        :param type: object
        :param name: perm 
        :param type: str
        
    
        :returns: bool
    """

    if (perm == 'comments'):
        return photo.can_comment
    elif (perm == 'meta'):
        return photo.can_addmeta

def increment_photo_meta_counts(photo, meta):
    """
        increment photo meta counts

        :param name: photo 
        :param type: object
        :param name: meta 
        :param type: str
        
    
        :returns: None
    """

    if (meta == 'notes'):
        photo.count_notes += 1
    elif (meta == 'comments'):
        photo.count_comments +=1
    elif (meta == 'tags'):
        photo.count_tags += 1
    elif (meta == 'people_tags'):
        photo.count_people_tagged += 1
    elif (meta== 'count_favourites'):
        photo.count_favourites += 1
    photo.save()


def decrement_photo_meta_counts(photo, meta):
    """
        decrement photo meta counts

        :param name: photo 
        :param type: object
        :param name: meta 
        :param type: str
        
    
        :returns: None
    """

    if (meta == 'notes'):
        photo.count_notes -= 1
    elif (meta == 'comments'):
        photo.count_comments -=1
    elif (meta == 'tags'):
        photo.count_tags -= 1
    elif (meta == 'people_tags'):
        photo.count_people_tagged -= 1
    elif (meta== 'count_favourites'):
        photo.count_favourites -= 1    
    
    photo.save()


def get_photo_meta_lists(id, meta):
    """
        get photo meta lists

        :param name: id 
        :param type: object
        :param name: meta 
        :param type: str
        
    
        :return: photo
        :return: people_tagged
    """

    if (meta == 'notes'):
        photo_notes = Note.objects.filter(photo_id = id)
        return photo_notes
    elif (meta == 'comments'):
        photo_comments = Comment.objects.filter(photo_id = id)
        return photo_comments
    elif (meta == 'tags'):
        photo_tags = Tag.objects.filter(photo_id = id)
        return photo_tags
    elif (meta == 'people_tags'):
        photo = Photo.objects.get(id=id)
        people_tagged = photo.people_tagged.all()
        return photo, people_tagged


def split_tags(request_data):
    """
        splits tags

        :param name: data 
        :param type: str
        
        
    
        :return: tags_text_list
        :return: obj
    """

    list = request_data['tag_text'].split()
    tags_text_list = []
    for tag_text in list:
        tags_text_list.append(tag_text.lower())
    return tags_text_list


def get_person_data(person):
    """
        get person data

        :param name: person 
        :param type: obj
        :return: person_data
        :return: data
    """
    person_data = {'id': person.id,
                          'email': person.email,
                          'username': person.username,
                          'first_name': person.first_name,
                          'last_name': person.last_name,
                          'age': person.age,
                          'is_pro': person.is_pro,
                          'login_from': person.login_from}
    return person_data



def delete_object(object):
    """
        delete object

        :param name: object 
        :param type: obj
        :returns: None
    """

    object.delete()


def save_object(object):
    """
        save object

        :param name: object 
        :param type: obj
        :returns: None
    """

    object.save()

def get_photos_of_the_followed_people(user):
    """
        Get photos of the followed people

        :param name: user 
        :param type: obj


        :return: following_photos
        :return: following_list_ids
    """
    following_list_ids = []
    following_list = user.follow_follower.all()
    for following in following_list:
        following_list_ids.append(following.followed.id)
    following_photos = Photo.objects.filter(is_public=True, owner_id__in=following_list_ids).order_by('-date_posted')
    return following_photos , following_list_ids


def get_photos_of_public_people(user):
    """
        Get photos of the public people

        :param name: user 
        :param type: obj


        :return: public_photos
    """
    _, following_list_ids= get_photos_of_the_followed_people(user)
    following_list_ids.append(user.id)
    ids_list = following_list_ids
    public_photos = Photo.objects.filter(is_public=True).exclude(owner_id__in=ids_list).order_by('-date_posted')
    return public_photos

    
def check_existence_of_media_file(data):
    """
        check existence of media file

        :param name: data 
        :param type: obj


        :return: bool
        :return: bool
        :return: message
        :return: str
        :return: response
        :return: str

    """
    bool=False
    message=''
    response=''
    if ('media_file' not in data):
        bool=True
        message = {'message': 'File is missing'}
        response = status.HTTP_400_BAD_REQUEST
    return bool,message ,response  

def upload(file_field,user,width,height):
    """
       get the type of the file from the extension

        :param name: file_field 
        :param type: obj
        :param name: user 
        :param type: obj
        :param name: width 
        :param type: obj
        :param name: height 
        :param type: obj


        :return: pixels
        :return: int
        :return: message
        :return: str
        :return: response
        :return: str
        :return: bool
        :return: message

    """
    # get the type of the file from the extension
    pixels=0
    bool=False
    message='uploaded'
    response = status.HTTP_201_CREATED  
    content_type = file_field.content_type.split('/')[0]
   
    # check if its type is image
    if content_type in settings.IMAGE_TYPE:
        # make limitations for the free user to have less than or equal 1000 media and 200mb as a max size of the photo
        pro= check_pro(user)
        if not pro :
            if user.total_media >= 1000:
                message= {'message': 'Exceeds media limit , Upgrade to pro'}
                response= status.HTTP_400_BAD_REQUEST
                return pixels, message,response,bool    
            elif file_field.size > settings.MAX_IMAGE_SIZE:
                message= {'message': 'Exceeds media size , Upgrade to pro'}
                response= status.HTTP_400_BAD_REQUEST
                return pixels, message,response,bool    


        # calculate the display pixels
        bool=True
        pixels = (250*int(width))/int(height)
    else:
        message= {'message': 'upload image file'}
        response = status.HTTP_400_BAD_REQUEST
    return pixels, message ,response,bool