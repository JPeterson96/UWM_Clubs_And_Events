from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class EditEvent(View):
    def get(self, request, id):
        current_user = user_util.User_Util.get_user(request.session['user'])

        try:
            event = Event.objects.get(pk=id)
            time = event.time_happening.strftime("%Y-%m-%dT%H:%M")
            request.session['oldname'] = event.name
            return render(request, "editevent.html", {"event": event, 'time': time, 'user': current_user})
        except:
            return render(request, "homepage.html", {"message": "Event does not exist", 'user': current_user})

    def post(self, request, id):

        event = Event.objects.get(pk=id)
        event.name = request.POST.get('name')

        # loc = event_util.Event_Util.verify_event_loc(request.POST.get('loc_addr'),
        #                                              request.POST.get('loc_city'),
        #                                              request.POST.get('loc_state'),
        #                                              request.POST.get('loc_zip'))
        # if isinstance(loc, ValueError):
        #     # does this work?
        #     return EditEvent.get(self, request=request, name=event.name)
        addr = request.POST.get('loc_addr')
        city = request.POST.get('loc_city')
        zip = request.POST.get('loc_zip')
        event.time_happening = request.POST.get('time_happening')
        event.description = request.POST.get('description')
        event.image = request.FILES.get('image')

        addr_check = event_util.Event_Util.verify_event_loc(addr, city, zip)
        if isinstance(addr_check, ValueError):
            return render(request, "editevent.html", {"event": event, 'time': event.time_happening})

        city_state = [part.strip() for part in city.split(',')]

        event.loc_addr = addr
        event.loc_city = city_state[0]
        event.loc_state = city_state[1]
        event.loc_zip = zip

        event.save()

        return render(request, "editevent.html", {'message': 'Event Information Changed Successfully!', 'event': event,
                                                  'time': event.time_happening})