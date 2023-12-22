from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class ViewEvent(View):
    def get(self, request, *args, **kwargs):
        eventname = kwargs["id"]
        actEvent = Event.objects.get(id=eventname)

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        print(current_user)
        print(actEvent.organization.user.email)

        try:
            event = Event.objects.get(id=eventname)
        except:
            return render(request, "homepage.html", {"message": "Event does not exist"})

        user_in_event = UserAttendEvent.objects.filter(user=current_user, event=actEvent)

        return render(request, "viewevent.html", {"Event": event, "user": current_user, "attend": user_in_event})

    def post(self, request, *args, **kwargs):
        eventname = kwargs["id"]
        actEvent = Event.objects.get(id=eventname)

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        user_in_event = UserAttendEvent.objects.filter(user=current_user, event=actEvent)
        if user_in_event.exists():
            unrsvp = request.POST.get('unrsvp')
            if unrsvp is not None:
                # delete if user wants
                user_in_event.get().delete()
                user_in_event = UserAttendEvent.objects.filter(user=current_user, event=actEvent)
                return render(request, "viewevent.html",
                              {"Event": actEvent, "user": current_user, "attend": user_in_event.exists()})
        else:
            rsvp = request.POST.get('rsvpbbut')
            print(rsvp)
            if rsvp is not None:
                UserAttendEvent.objects.create(user=current_user, event=actEvent)
                user_in_event = UserAttendEvent.objects.filter(user=current_user, event=actEvent)
                return render(request, "viewevent.html",
                              {"Event": actEvent, "user": current_user, "attend": user_in_event.exists()})