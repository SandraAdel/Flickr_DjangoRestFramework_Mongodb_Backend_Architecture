import json

from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse
from django.test import TestCase, Client, TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import *
from .models import *
from .serializers import *
from .views import *
from .urls import *
from django.core.files import File
import datetime
from .views_functions import *
from project.permissions import check_permission
from accounts.views import verifying_user
import time
from PIL import Image
import os



# Creating a test user function for running tests
def create_test_user(email, first_name, last_name, password, age):

    user = Account.objects.create_user(email, first_name, last_name, age, password)
    verifying_user(user)
    return user 


# SERIALIZER TESTS


# PhotoPermSerializer Tests
class TestsThatDependsOnPrimaryKeySequences(TransactionTestCase):
    reset_sequences = True


    def test_change_perms_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=False, can_comment='Only The Owner', can_addmeta='Only The Owner')
        new_perms = {'is_public': True, 'can_comment': 'Any Flickr Member', 'can_addmeta': 'People You Follow'}
        new_photo = PhotoPermSerializer(photo, data=new_perms)
        self.assertEqual(new_photo.is_valid(), True)
        new_photo.save()
        self.assertEqual(photo.is_public, True)
        self.assertEqual(photo.can_comment,  'Any Flickr Member')
        self.assertEqual(photo.can_addmeta, 'People You Follow')

    def test_change_perms_invalid_ispublic_input(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=False, can_comment='Only The Owner', can_addmeta='Only The Owner')
        new_perms = {'is_public': 123}
        new_photo = PhotoPermSerializer(photo, data=new_perms)
        self.assertEqual(new_photo.is_valid(), False)
        self.assertEqual(new_photo.errors['is_public'][0], "Must be a valid boolean.")
    
    def test_change_perms_invalid_cancomment_input(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=False, can_comment='Only The Owner', can_addmeta='Only The Owner')
        new_perms = {'can_comment': True}
        new_photo = PhotoPermSerializer(photo, data=new_perms)
        self.assertEqual(new_photo.is_valid(), False)
        self.assertEqual(new_photo.errors['can_comment'][0], '\"True\" is not a valid choice.')

    def test_change_perms_invalid_canaddmeta_input(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=False, can_comment='Only The Owner', can_addmeta='Only The Owner')
        new_perms = {'can_addmeta': 'Owner'}
        new_photo = PhotoPermSerializer(photo, data=new_perms)
        self.assertEqual(new_photo.is_valid(), False)
        self.assertEqual(new_photo.errors['can_addmeta'][0], '\"Owner\" is not a valid choice.')
    

# PhotoMetaSerializer Tests
class TestPhotoMetaSerializer(TestCase):

    def test_change_meta_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, title='Flowers', description='These are my flowers')
        new_meta = {'title': 'New Flowers', 'description': 'These are my new flowers'}
        new_photo = PhotoMetaSerializer(photo, data=new_meta)
        self.assertEqual(new_photo.is_valid(), True)
        new_photo.save()
        self.assertEqual(photo.title,  'New Flowers')
        self.assertEqual(photo.description, 'These are my new flowers')

    def test_change_meta_invalid_title_input(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, title='Flowers', description='These are my flowers')
        new_title = ''
        for i in range (28):
            new_title = new_title + '_new_title_'
        new_meta = {'title': new_title}
        new_photo = PhotoMetaSerializer(photo, data=new_meta)
        self.assertEqual(new_photo.is_valid(), False)
        self.assertEqual(new_photo.errors['title'][0], 'Ensure this field has no more than 300 characters.')

    def test_change_meta_invalid_title_description(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, title='Flowers', description='These are my flowers')
        new_description = ''
        for i in range (120):
            new_description = new_description + '_new_description_'
        new_meta = {'description': new_description}
        new_photo = PhotoMetaSerializer(photo, data=new_meta)
        self.assertEqual(new_photo.is_valid(), False)
        self.assertEqual(new_photo.errors['description'][0], 'Ensure this field has no more than 2000 characters.')


# PhotoDatesSerializer Tests
class TestPhotoDatesSerializer(TestCase):

    def test_change_dates_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, date_taken=datetime.datetime.now(datetime.timezone.utc))
        time.sleep(1)
        new_date = datetime.datetime.now(datetime.timezone.utc)
        new_dates = {'date_taken': new_date}
        new_photo = PhotoDatesSerializer(photo, data=new_dates)
        self.assertEqual(new_photo.is_valid(), True)
        new_photo.save()
        self.assertEqual(photo.date_taken, new_date)
        
    def test_change_dates_invalid_date(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, date_taken=datetime.datetime.now(datetime.timezone.utc))
        new_dates = {'date_taken': '2021/05/01 05:00:00'}
        new_photo = PhotoDatesSerializer(photo, data=new_dates)
        self.assertEqual(new_photo.is_valid(), False)
        self.assertEqual(new_photo.errors['date_taken'][0],  "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].")


# PhotoCommentSerializer Tests
class TestPhotoCommentSerializer(TestCase):

    def test_create_comment_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_comment_data = {'comment_text': 'This is a new comment'}
        created_comment = PhotoCommentSerializer(data=created_comment_data)
        self.assertEqual(created_comment.is_valid(), True)
        created_comment.save(author=user, photo=photo)
        comment = Comment.objects.get(author=user)
        self.assertEqual(comment.comment_text, 'This is a new comment')

    def test_create_comment_invalid_comment_text(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        comment_text = ''
        for i in range (44):
            comment_text = comment_text + ' This is a new comment '
        created_comment_data = {'comment_text': comment_text}
        created_comment = PhotoCommentSerializer(data=created_comment_data)
        self.assertEqual(created_comment.is_valid(), False)
        self.assertEqual(created_comment.errors['comment_text'][0], 'Ensure this field has no more than 1000 characters.')

    def test_create_comment_missing_arguments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_comment_data = {}
        created_comment = PhotoCommentSerializer(data=created_comment_data)
        self.assertEqual(created_comment.is_valid(), False)
        self.assertEqual(created_comment.errors['comment_text'][0], "This field is required.")

    def test_edit_comment(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        comment = Comment.objects.create(author=user, comment_text='This is a comment', photo=photo)
        new_comment_data = {'comment_text': 'This is a new comment text'}
        edited_comment = PhotoCommentSerializer(comment, data=new_comment_data)
        self.assertEqual(edited_comment.is_valid(), True)
        edited_comment.save()
        self.assertEqual(comment.comment_text, 'This is a new comment text')

    def test_delete_comment(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_comment_data = {'comment_text': 'This is a comment'}
        created_comment = PhotoCommentSerializer(data=created_comment_data)
        self.assertEqual(created_comment.is_valid(), True)
        created_comment.save(author=user, photo=photo)
        comment = Comment.objects.get(author=user)
        comment.delete()
        comment = Comment.objects.filter(author=user)
        self.assertEqual(comment.exists(), False)


# PhotoNoteSerializer Tests
class TestPhotoNoteSerializer(TestCase):

    def test_create_note_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_note_data = {'left_coord': 0, 'top_coord': 0, 'note_width': 50, 'note_height': 50, 'note_text': 'This is a new note'}
        created_note = PhotoNoteSerializer(data=created_note_data)
        self.assertEqual(created_note.is_valid(), True)
        created_note.save(author=user, photo=photo)
        note = Note.objects.get(author=user)
        self.assertEqual(note.left_coord, 0)
        self.assertEqual(note.top_coord, 0)
        self.assertEqual(note.note_width, 50)
        self.assertEqual(note.note_height, 50)
        self.assertEqual(note.note_text, 'This is a new note')

    def test_create_note_invalid_coordinates(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_note_data = {'left_coord': 'left', 'top_coord': 'top', 'note_width': 50, 'note_height': 50, 'note_text': 'This is a new note'}
        created_note = PhotoNoteSerializer(data=created_note_data)
        self.assertEqual(created_note.is_valid(), False)
        self.assertEqual(created_note.errors['left_coord'][0], "A valid integer is required.")
        self.assertEqual(created_note.errors['top_coord'][0], "A valid integer is required.")

    
    def test_create_note_invalid_dimensions(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_note_data = {'left_coord': 0, 'top_coord': 0, 'note_width': -50, 'note_height': -50, 'note_text': 'This is a new note'}
        created_note = PhotoNoteSerializer(data=created_note_data)
        self.assertEqual(created_note.is_valid(), False)
        self.assertEqual(created_note.errors['note_width'][0], "Ensure this value is greater than or equal to 0.")
        self.assertEqual(created_note.errors['note_height'][0], "Ensure this value is greater than or equal to 0.")

    def test_create_comment_invalid_note_text(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        note_text = ''
        for i in range (53):
            note_text = note_text + ' This is a new note '
        created_note_data = {'note_text': note_text}
        created_note = PhotoNoteSerializer(data=created_note_data)
        self.assertEqual(created_note.is_valid(), False)
        self.assertEqual(created_note.errors['note_text'][0], 'Ensure this field has no more than 1000 characters.')

    def test_create_note_missing_arguments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_note_data = {'left_coord': 0, 'top_coord': 0, 'note_width': 50, 'note_height': 50}
        created_note = PhotoNoteSerializer(data=created_note_data)
        self.assertEqual(created_note.is_valid(), False)
        self.assertEqual(created_note.errors['note_text'][0], "This field is required.")

    def test_edit_note(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        note = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is a note', photo=photo)
        new_note_data = {'left_coord': 50, 'top_coord': 50, 'note_width': 100, 'note_height': 100, 'note_text': 'This is a new note'}
        edited_note = PhotoNoteSerializer(note, data=new_note_data)
        self.assertEqual(edited_note.is_valid(), True)
        edited_note.save()
        self.assertEqual(note.left_coord, 50)
        self.assertEqual(note.top_coord, 50)
        self.assertEqual(note.note_width, 100)
        self.assertEqual(note.note_height, 100)
        self.assertEqual(note.note_text, 'This is a new note')

    def test_delete_note(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_note_data = {'left_coord': 0, 'top_coord': 0, 'note_width': 50, 'note_height': 50, 'note_text': 'This is a new note'}
        created_note = PhotoNoteSerializer(data=created_note_data)
        self.assertEqual(created_note.is_valid(), True)
        created_note.save(author=user, photo=photo)
        note = Note.objects.get(author=user)
        note.delete()
        note = Note.objects.filter(author=user)
        self.assertEqual(note.exists(), False)


# PhotoTagSerializer Tests
class TestPhotoTagSerializer(TestCase):

    def test_create_tag_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_tag_data = {'tag_text': 'nature'}
        created_tag = PhotoTagSerializer(data=created_tag_data)
        self.assertEqual(created_tag.is_valid(), True)
        created_tag.save(author=user, photo=photo)
        tag = Tag.objects.get(author=user)
        self.assertEqual(tag.tag_text, 'nature')

    def test_create_tag_missing_arguments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_tag_data = {}
        created_tag = PhotoTagSerializer(data=created_tag_data)
        self.assertEqual(created_tag.is_valid(), False)
        self.assertEqual(created_tag.errors['tag_text'][0], "This field is required.")

    def test_create_tag_invalid_tag_text(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        tag_text = ''
        for i in range (41):
            tag_text = tag_text + ' tag '
        created_tag_data = {'tag_text': tag_text}
        created_tag = PhotoTagSerializer(data=created_tag_data)
        self.assertEqual(created_tag.is_valid(), False)
        self.assertEqual(created_tag.errors['tag_text'][0], 'Ensure this field has no more than 200 characters.')

    def test_delete_tag(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        created_tag_data = {'tag_text': 'nature'}
        created_tag = PhotoTagSerializer(data=created_tag_data)
        self.assertEqual(created_tag.is_valid(), True)
        created_tag.save(author=user, photo=photo)
        tag = Tag.objects.get(author=user)
        tag.delete()
        tag = Tag.objects.filter(author=user)
        self.assertEqual(tag.exists(), False)


# PeopleTaggingSerializer Tests
class TestPeopleTaggingSerializer(TestCase):

    def test_tag_person_normal_case(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()
        relation = PeopleTagging.objects.get(photo=photo)
        self.assertEqual(relation.photo, photo)
        self.assertEqual(relation.person_tagged, user2)
        self.assertEqual(relation.added_by, user1)

    def test_tag_person_missing_arguments(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), False)
        self.assertEqual(created_relation.errors['added_by'][0], "This field is required.")

    def test_untag_person(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()
        relation = PeopleTagging.objects.get(photo=photo)
        relation.delete()
        relation = PeopleTagging.objects.filter(photo=photo)
        self.assertEqual(relation.exists(), False)


# PhotoRotationSerializer Tests
class TestPhotoRotationSerializer(TestCase):

    def test_change_rotated_by_normal_case(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        rotation_data = {'rotated_by': 90}
        rotated_photo = PhotoRotationSerializer(photo, data=rotation_data)
        self.assertEqual(rotated_photo.is_valid(), True)
        rotated_photo.save()
        self.assertEqual(photo.rotated_by, 90)

    def test_change_rotated_by_invalid_angle(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        rotation_data = {'rotated_by': -90}
        rotated_photo = PhotoRotationSerializer(photo, data=rotation_data)
        self.assertEqual(rotated_photo.is_valid(), False)
        self.assertEqual(rotated_photo.errors['rotated_by'][0], "Ensure this value is greater than or equal to 0.")



# PHOTO FUNCTION TESTS


# search_according_to_all_or_tags Function
class TestSearchAccordingToAllOrTagsFunction(TestCase):

    def test_search_according_to_all_or_tags_without_all_or_tags_input(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True, title='moon light')
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True, description='lily flower')
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        created_tag_data = {'tag_text': 'camera'}
        created_tag = PhotoTagSerializer(data=created_tag_data)
        self.assertEqual(created_tag.is_valid(), True)
        created_tag.save(author=user1, photo=photo3)

        request_data = {'search_text': 'moon flower camera'}
        photo_ids_list = search_according_to_all_or_tags(request_data)

        self.assertEqual(photo_ids_list[0], photo1.id)
        self.assertEqual(photo_ids_list[1], photo2.id)
        self.assertEqual(photo_ids_list[2], photo3.id)

    def test_search_according_to_all_or_tags_with_all(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True, title='moon light')
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True, description='lily flower')
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        created_tag_data = {'tag_text': 'camera', 'all_or_tags': 'all'}
        created_tag = PhotoTagSerializer(data=created_tag_data)
        self.assertEqual(created_tag.is_valid(), True)
        created_tag.save(author=user1, photo=photo3)

        request_data = {'search_text': 'moon flower camera', 'all_or_tags': 'all'}
        photo_ids_list = search_according_to_all_or_tags(request_data)

        self.assertEqual(photo_ids_list[0], photo1.id)
        self.assertEqual(photo_ids_list[1], photo2.id)
        self.assertEqual(photo_ids_list[2], photo3.id)
    
    def test_search_according_to_all_or_tags_with_tags(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True, title='moon light')
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True, description='lily flower')
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo4 = Photo.objects.create(media_file='126.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        created_tag_data1 = {'tag_text': 'camera'}
        created_tag1 = PhotoTagSerializer(data=created_tag_data1)
        self.assertEqual(created_tag1.is_valid(), True)
        created_tag1.save(author=user1, photo=photo3)

        created_tag_data2 = {'tag_text': 'star'}
        created_tag2 = PhotoTagSerializer(data=created_tag_data2)
        self.assertEqual(created_tag2.is_valid(), True)
        created_tag2.save(author=user1, photo=photo4)

        request_data = {'search_text': 'moon flower camera star', 'all_or_tags': 'tags'}
        photo_ids_list = search_according_to_all_or_tags(request_data)

        self.assertEqual(photo_ids_list[0], photo3.id)
        self.assertEqual(photo_ids_list[1], photo4.id)

    def test_search_according_to_all_or_tags_with_invalid_all_or_tags_input(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True, title='moon light')
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True, description='lily flower')

        request_data = {'search_text': 'moon flower', 'all_or_tags': 'ddd'}
        photo_ids_list = search_according_to_all_or_tags(request_data)

        self.assertEqual(photo_ids_list, None)


# filter_by_date Function
class TestFilterByDateFunction(TestCase):

    def test_filter_by_date_not_anonymous_upload_date(self):
        
        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        time.sleep( 1 )
        min_upload_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )

        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo4 = Photo.objects.create(media_file='126.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        time.sleep( 1 )
        max_upload_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )

        photo5 = Photo.objects.create(media_file='127.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        user_photos = Photo.objects.filter(id=photo3.id) | Photo.objects.filter(id=photo2.id) | Photo.objects.filter(id=photo1.id)
        following_photos = Photo.objects.filter(id=50)
        everyone_photos = Photo.objects.filter(id=photo5.id) | Photo.objects.filter(id=photo4.id)

        user_photos, following_photos, everyone_photos = filter_by_date(False, 'upload_date', min_upload_date, max_upload_date, user_photos, following_photos, everyone_photos)
        self.assertEqual(user_photos.count(), 2)
        self.assertEqual(following_photos.count(), 0)
        self.assertEqual(everyone_photos.count(), 1)
        user_photos = list(user_photos)
        following_photos = list(following_photos)
        everyone_photos = list(everyone_photos)
        self.assertEqual(user_photos[0], photo2)
        self.assertEqual(user_photos[1], photo3)
        self.assertEqual(everyone_photos[0], photo4)
    
    def test_filter_by_date_anonymous_upload_date(self):
        
        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        time.sleep( 1 )
        min_upload_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )

        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        time.sleep( 1 )
        max_upload_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )

        photo4 = Photo.objects.create(media_file='126.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        user_photos = Photo.objects.filter(id=60)
        following_photos = Photo.objects.filter(id=80)
        everyone_photos = Photo.objects.filter(id=photo1.id) | Photo.objects.filter(id=photo2.id) | Photo.objects.filter(id=photo3.id)

        user_photos, following_photos, everyone_photos = filter_by_date(True, 'upload_date', min_upload_date, max_upload_date, user_photos, following_photos, everyone_photos)
        self.assertEqual(user_photos.count(), 0)
        self.assertEqual(following_photos.count(), 0)
        self.assertEqual(everyone_photos.count(), 2)
        user_photos = list(user_photos)
        following_photos = list(following_photos)
        everyone_photos = list(everyone_photos)
        self.assertEqual(everyone_photos[0], photo2)
        self.assertEqual(everyone_photos[1], photo3)

    def test_filter_by_date_not_anonymous_taken_date(self):
    
        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')

        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        time.sleep( 1 )
        min_taken_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        photo4 = Photo.objects.create(media_file='126.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        time.sleep( 1 )
        max_taken_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )
        photo5 = Photo.objects.create(media_file='127.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))

        user_photos = Photo.objects.filter(id=photo3.id) | Photo.objects.filter(id=photo2.id) | Photo.objects.filter(id=photo1.id)
        following_photos = Photo.objects.filter(id=16)
        everyone_photos = Photo.objects.filter(id=photo5.id) | Photo.objects.filter(id=photo4.id)

        user_photos, following_photos, everyone_photos = filter_by_date(False, 'taken_date', min_taken_date, max_taken_date, user_photos, following_photos, everyone_photos)
        self.assertEqual(user_photos.count(), 2)
        self.assertEqual(following_photos.count(), 0)
        self.assertEqual(everyone_photos.count(), 1)
        user_photos = list(user_photos)
        following_photos = list(following_photos)
        everyone_photos = list(everyone_photos)
        self.assertEqual(user_photos[0], photo2)
        self.assertEqual(user_photos[1], photo3)
        self.assertEqual(everyone_photos[0], photo4)

    def test_filter_by_date_anonymous_taken_date(self):
    
        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')

        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        time.sleep( 1 )
        min_taken_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))
        time.sleep( 1 )
        max_taken_date = datetime.datetime.now(datetime.timezone.utc)
        time.sleep( 1 )
        photo4 = Photo.objects.create(media_file='126.png', photo_height=123, photo_width=22, owner=user1, is_public=True, date_taken=datetime.datetime.now(datetime.timezone.utc))

        user_photos = Photo.objects.filter(id=5)
        following_photos = Photo.objects.filter(id=6)
        everyone_photos = Photo.objects.filter(id=photo1.id) | Photo.objects.filter(id=photo2.id) | Photo.objects.filter(id=photo3.id)

        user_photos, following_photos, everyone_photos = filter_by_date(True, 'taken_date', min_taken_date, max_taken_date, user_photos, following_photos, everyone_photos)
        self.assertEqual(user_photos.count(), 0)
        self.assertEqual(following_photos.count(), 0)
        self.assertEqual(everyone_photos.count(), 2)
        user_photos = list(user_photos)
        following_photos = list(following_photos)
        everyone_photos = list(everyone_photos)
        self.assertEqual(everyone_photos[0], photo2)
        self.assertEqual(everyone_photos[1], photo3)


# photo search functions related to search_photos API
# search_in_search_place, get_search_photos_anonymous_case Function Tests
class TestPhotoSearchFunctions(TestCase):

    def test_search_in_search_place(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user2, is_public=True)

        user_photos, following_photos, everyone_photos = search_in_search_place([photo3.id, photo2.id, photo1.id], user1)
        user_photos = list(user_photos)
        following_photos = list(following_photos)
        everyone_photos = list(everyone_photos)

        self.assertEqual(user_photos[0], photo2)
        self.assertEqual(user_photos[1], photo1)
        self.assertEqual(following_photos, [])
        self.assertEqual(everyone_photos[0], photo3)

    def test_get_search_photos_anonymous_case(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        user_photos, following_photos, everyone_photos = get_search_photos_anonymous_case()
        user_photos = list(user_photos)
        following_photos = list(following_photos)
        everyone_photos = list(everyone_photos)
        self.assertEqual(user_photos, [])
        self.assertEqual(following_photos, [])
        self.assertEqual(everyone_photos[0], photo3)
        self.assertEqual(everyone_photos[1], photo2)
        self.assertEqual(everyone_photos[2], photo1)


# get_required_photo, get_required_comment_and_its_photo, get_required_note_and_its_photo
# get_required_tag_and_its_photo, get_photo_and_person_tagged, test_get_photo_permission
# Functions Tests
class TestDataAccessFunctions(TestCase):

    def test_get_required_photo(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True)
        self.assertEqual(get_required_photo(photo.id), photo)

    def test_get_required_comment_and_its_photo(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True)
        comment = Comment.objects.create(author=user, comment_text='This is a comment', photo=photo)
        output_comment, output_photo_id, output_photo = get_required_comment_and_its_photo(comment.comment_id)
        self.assertEqual(output_comment, comment)
        self.assertEqual(output_photo, photo)
        self.assertEqual(output_photo_id, photo.id)

    def test_get_required_note_and_its_photo(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True)
        note = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is a note', photo=photo)
        output_note, output_photo_id, output_photo = get_required_note_and_its_photo(note.note_id)
        self.assertEqual(output_note, note)
        self.assertEqual(output_photo, photo)
        self.assertEqual(output_photo_id, photo.id)

    def test_get_required_tag_and_its_photo(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True)
        tag = Tag.objects.create(author=user, tag_text='nature', photo=photo)
        output_tag, output_photo = get_required_tag_and_its_photo(tag.tag_id)
        self.assertEqual(output_tag, tag)
        self.assertEqual(output_photo, photo)

    def test_get_photo_and_person_tagged(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()
        output_photo, person_tagged = get_photo_and_person_tagged(photo.id, user2.id)
        self.assertEqual(person_tagged, user2)
        self.assertEqual(output_photo, photo)

    def test_get_photo_permission(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True, can_comment='People You Follow', can_addmeta='Only The Owner')
        self.assertEqual(get_photo_permission(photo, 'comments'), 'People You Follow')
        self.assertEqual(get_photo_permission(photo, 'meta'), 'Only The Owner')


# get_photo_meta_lists Function Tests
class TestGetPhotoMetaListsFunction(TestCase):

    def test_get_photo_meta_lists_notes(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        note1 = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is the first note', photo=photo)
        note2 = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is the second note', photo=photo)
        note3 = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is the third note', photo=photo)
        notes = get_photo_meta_lists(photo.id, 'notes')
        self.assertEqual(notes.count(), 3)
        notes = list(notes)
        self.assertEqual(notes[0], note1)
        self.assertEqual(notes[1], note2)
        self.assertEqual(notes[2], note3)

    def test_get_photo_meta_lists_comments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        comment1 = Comment.objects.create(author=user, comment_text='This is the first comment', photo=photo)
        comment2 = Comment.objects.create(author=user, comment_text='This is the second comment', photo=photo)
        comment3 = Comment.objects.create(author=user, comment_text='This is the third comment', photo=photo)
        comments = get_photo_meta_lists(photo.id, 'comments')
        self.assertEqual(comments.count(), 3)
        comments = list(comments)
        self.assertEqual(comments[0], comment1)
        self.assertEqual(comments[1], comment2)
        self.assertEqual(comments[2], comment3)

    def test_get_photo_meta_lists_comments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        tag1 = Tag.objects.create(author=user, tag_text='nature', photo=photo)
        tag2 = Tag.objects.create(author=user, tag_text='flower', photo=photo)
        tag3 = Tag.objects.create(author=user, tag_text='sun', photo=photo)
        tags = get_photo_meta_lists(photo.id, 'tags')
        self.assertEqual(tags.count(), 3)
        tags = list(tags)
        self.assertEqual(tags[0], tag1)
        self.assertEqual(tags[1], tag2)
        self.assertEqual(tags[2], tag3)

    def test_get_photo_meta_lists_people_tags(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)

        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()

        user3 = create_test_user('adamharts@yahoo.com', 'Adam', 'Harts', 'Adam12345678', '20')
        tag_person_data = {'photo': photo.id, 'person_tagged': user3.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()

        photo, people_tagged = get_photo_meta_lists(photo.id, 'people_tags')
        self.assertEqual(len(people_tagged), 2)
        self.assertEqual(people_tagged[0].person_tagged, user2)
        self.assertEqual(people_tagged[1].person_tagged, user3)


# increment_photo_meta_counts Function Tests
class TestIncrementPhotoMetaCountsFunction(TestCase):

    def test_increment_photo_meta_counts_notes(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        note = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is a note', photo=photo)
        increment_photo_meta_counts(photo, 'notes')
        self.assertEqual(photo.count_notes, 1)

    def test_increment_photo_meta_counts_comments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        comment = Comment.objects.create(author=user, comment_text='This is a comment', photo=photo)
        increment_photo_meta_counts(photo, 'comments')
        self.assertEqual(photo.count_comments, 1)

    def test_increment_photo_meta_counts_tags(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        tag = Tag.objects.create(author=user, tag_text='nature', photo=photo)
        increment_photo_meta_counts(photo, 'tags')
        self.assertEqual(photo.count_tags, 1)

    def test_increment_photo_meta_counts_people_tags(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()
        increment_photo_meta_counts(photo, 'people_tags')
        self.assertEqual(photo.count_people_tagged, 1)


# decrement_photo_meta_counts Function Tests
class TestDecrementPhotoMetaCountsFunction(TestCase):

    def test_decrement_photo_meta_counts_notes(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        note = Note.objects.create(author=user, left_coord=0, top_coord=0, note_width=50, note_height=50, note_text='This is a note', photo=photo)
        increment_photo_meta_counts(photo, 'notes')
        note.delete()
        decrement_photo_meta_counts(photo, 'notes')
        self.assertEqual(photo.count_notes, 0)

    def test_deccrement_photo_meta_counts_comments(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        comment = Comment.objects.create(author=user, comment_text='This is a comment', photo=photo)
        increment_photo_meta_counts(photo, 'comments')
        comment.delete()
        decrement_photo_meta_counts(photo, 'comments')
        self.assertEqual(photo.count_comments, 0)

    def test_decrement_photo_meta_counts_tags(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        tag = Tag.objects.create(author=user, tag_text='nature', photo=photo)
        increment_photo_meta_counts(photo, 'tags')
        tag.delete()
        decrement_photo_meta_counts(photo, 'tags')
        self.assertEqual(photo.count_tags, 0)

    def test_decrement_photo_meta_counts_people_tags(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1)
        user2 = create_test_user('johnsmith22@yahoo.com', 'John', 'Smith', 'John12345678', '18')
        tag_person_data = {'photo': photo.id, 'person_tagged': user2.id, 'added_by': user1.id}
        created_relation = PeopleTaggingSerializer(data=tag_person_data)
        self.assertEqual(created_relation.is_valid(), True)
        created_relation.save()
        increment_photo_meta_counts(photo, 'people_tags')
        relation = PeopleTagging.objects.get(photo=photo)
        relation.delete()
        decrement_photo_meta_counts(photo, 'people_tags')
        self.assertEqual(photo.count_people_tagged, 0)


# remove_photo_path_locally, limit_photos_number Functions Tests
class TestMiscellaneousFunctions(TestCase):

    def test_limit_photos_number(self):

        user1 = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo1 = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo2 = Photo.objects.create(media_file='124.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo3 = Photo.objects.create(media_file='125.png', photo_height=123, photo_width=22, owner=user1, is_public=True)
        photo4 = Photo.objects.create(media_file='126.png', photo_height=123, photo_width=22, owner=user1, is_public=True)

        photos = [photo1, photo2, photo3, photo4]
        self.assertEqual(len(photos), 4)
        limited_photos = limit_photos_number(photos, 2)
        self.assertEqual(limited_photos.count(), 2)
    
    def test_remove_photo_path_locally(self):
    
        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        img = Image.new('RGB', (60, 60), color = 'red')
        if not os.path.exists('media'):
            os.makedirs('media')
        img.save(os.path.join('media', "123.png"))
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True)
        self.assertEqual(os.path.isfile('media/123.png'), True)
        remove_photo_path_locally(photo)
        photo.delete()
        self.assertEqual(os.path.isfile('media/123.png'), False)


# Saving and Deleting Objects Functions Tests
class TestSaveAndDeleteObjectsFunctions(TestCase):

    def test_delete_object(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', 21)
        user = Account.objects.filter(id=user.id)
        self.assertEqual(user.exists(), True)
        delete_object(user)
        self.assertEqual(user.exists(), False)

    def test_save_object(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        self.assertEqual(photo.is_public, True)
        new_photo = PhotoPermSerializer(photo, data={'is_public': False})
        self.assertEqual(new_photo.is_valid(), True)
        save_object(new_photo)
        self.assertEqual(photo.is_public, False)


# get_note_coordinates, split_tags, get_person_data
# Functions Tests
class TestHandlingRequestDataFunctions(TestCase):

    def test_get_note_coordinates(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user, is_public=True)
        new_note_data = {'left_coord': 0, 'top_coord': 50, 'note_width': 100, 'note_height': 150, 'note_text': 'This is a new note'}
        created_note = PhotoNoteSerializer(data=new_note_data)
        self.assertEqual(created_note.is_valid(), True)
        created_note.save(author=user, photo=photo)
        left_coord, top_coord, note_width, note_height = get_note_coordinates(new_note_data)
        self.assertEqual(left_coord, 0)
        self.assertEqual(top_coord, 50)
        self.assertEqual(note_width, 100)
        self.assertEqual(note_height, 150)

    def test_split_tags(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', '21')
        photo = Photo.objects.create(media_file='123.png', photo_height=123, photo_width=22, owner=user)
        request_data = {'tag_text': 'NATURE flOWEr MoOn'}
        tags_text_list = split_tags(request_data)
        for text in tags_text_list:
            Tag.objects.create(author=user, tag_text=text, photo=photo)
        tags = Tag.objects.filter(photo_id=photo.id)
        tags = list(tags)
        self.assertEqual(tags[0].tag_text, 'nature')
        self.assertEqual(tags[1].tag_text, 'flower')
        self.assertEqual(tags[2].tag_text, 'moon')

    def test_get_person_data(self):

        user = create_test_user('sandraadel99@yahoo.com', 'Sandra', 'Adel', 'Sandra123456', 21)
        person_data = get_person_data(user)
        self.assertEqual(person_data['id'], user.id)
        self.assertEqual(person_data['email'], 'sandraadel99@yahoo.com')
        self.assertEqual(person_data['first_name'], 'Sandra')
        self.assertEqual(person_data['last_name'], 'Adel')
        self.assertEqual(person_data['age'], 21)
        self.assertEqual(person_data['is_pro'], False)
        self.assertEqual(person_data['login_from'], 'email')


def create_user_test(email):
    #prepare user
    first_name = 'test2'
    last_name = 'name'
    age = '50'
    password = 'Caroline1234567'
    email = email
    Account.objects.create_user(email,first_name,last_name,age,password)
    user=Account.objects.get(email = email)
    verifying_user(user)
    return user 

class PhotoFunctionsTests(TestCase):   

    def test_get_photos_of_the_followed_people(self):    
        user=create_user_test('user99@gmail.com')
        owner=create_user_test('owner998@gmail.com')
        Contacts.objects.create(user=user,followed=owner)
        Photo.objects.create(media_file='api/media/1236.png',photo_height=123,photo_width=22,owner=owner)
        following_photos,_ =get_photos_of_the_followed_people(user)
        self.assertEqual(following_photos.exists(),True)
    
    def test_get_photos_of_the_followed_people_failure(self):    
        user=create_user_test('user2@gmail.com')
        owner=create_user_test('owner2@gmail.com')
        Contacts.objects.create(user=user,followed=owner)
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        following_photos,_ =get_photos_of_the_followed_people(user)
        self.assertEqual(following_photos.exists(), False )    

    def test_get_photos_of_the_public_people_success(self):    
        user=create_user_test('user@gmail.com')
        owner=create_user_test('owner@gmail.com')
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22, is_public=True, owner=owner)
        photo_obj=Photo.objects.all().first()
        public_photos = get_photos_of_public_people(user)
        self.assertEqual(public_photos.first(),photo_obj )    


    def test_get_photos_of_the_public_people_failure(self):    
        user=create_user_test('user@gmail.com')
        owner=create_user_test('owner@gmail.com')
        Contacts.objects.create(user=user,followed=owner)
        Photo.objects.create(media_file='api/media/123.png',photo_height=123,photo_width=22,owner=user)
        public_photos = get_photos_of_public_people(user)
        self.assertEqual(public_photos.first(),None )

