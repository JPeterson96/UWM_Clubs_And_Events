from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Interest)
admin.site.register(StudentInterest)
admin.site.register(EventTag)
admin.site.register(Major)
admin.site.register(StudentMajor)
admin.site.register(Organization)
admin.site.register(MembersIn)
admin.site.register(Calendar)
admin.site.register(UserAttendEvent)
