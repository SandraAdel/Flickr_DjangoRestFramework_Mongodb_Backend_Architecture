from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Gallery)
admin.site.register(Comments)
