from django.contrib import admin
from .models import User, Event, UserInterest, EventTag, Interest

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Interest)
admin.site.register(UserInterest)
admin.site.register(EventTag)
