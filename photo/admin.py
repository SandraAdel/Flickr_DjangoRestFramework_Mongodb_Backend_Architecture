from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(PeopleTagging)
admin.site.register(Tag)
