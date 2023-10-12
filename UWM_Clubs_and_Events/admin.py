from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Interest)
admin.site.register(UserInterest)
admin.site.register(EventTag)
admin.site.register(Major)
admin.site.register(UserMajor)
admin.site.register(Organization)
admin.site.register(MembersIn)
