from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([group])
admin.site.register([topic])
admin.site.register([reply])
admin.site.register([Members])
admin.site.register([PendingMembers])
