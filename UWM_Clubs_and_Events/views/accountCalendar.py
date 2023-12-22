from django.shortcuts import render
from django.views import View

from UWM_Clubs_and_Events.models import *
from classes import user_util


class accountCalendar(View):
    def get(self, request):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        all_events = Event.objects.all()
        return render(request, "accountCalendar.html",
                      {"name": 'accountCalendar', 'events': all_events, 'user': current_user})