from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class CreateEvent(View):
    def get(self, request):
        tags = Interest.objects.all()
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        if current_user.role == 2:
            orgs = Organization.objects.filter(user__exact=current_user)
        else:
            orgs = Organization.objects.filter(point_of_contact__exact=current_user.email)
        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)
        return render(request, "createevent.html",
                      {"interests": filtered_interests, "orgs": orgs, "user": current_user, })

    def post(self, request):
        tags = Interest.objects.all()
        search = request.GET.get('search-input', '')

        name = request.POST.get('name')
        org_name = request.POST.get('org')

        time_happening = request.POST.get('time-happening')
        description = request.POST.get('description')
        time_published = datetime.now()
        photo = request.FILES.get('photo')
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        orgs = Organization.objects.filter(point_of_contact__exact=current_user.email)
        search = request.GET.get('search-input', '')
        filtered_interests = Interest.objects.filter(tag__icontains=search)

        try:
            selected_org = Organization.objects.get(name=org_name)
        except Organization.DoesNotExist:
            return render(request, "createevent.html",
                          {"interests": filtered_interests, "orgs": orgs, "user": current_user,
                           "message": "Selected organization does not exist"})

        addr = request.POST.get('loc_addr')
        city = request.POST.get('loc_city')
        zip = request.POST.get('loc_zip')

        addr_check = event_util.Event_Util.verify_event_loc(addr, city, zip)
        if isinstance(addr_check, ValueError):
            return render(request, "createevent.html",
                          {'name': name, 'loc_addr': addr, 'loc_zip': zip, "interests": filtered_interests,
                           "description": description, "orgs": orgs, "user": current_user,
                           "time": time_happening, "message": addr_check})

        city_state = [part.strip() for part in city.split(',')]
        city_name = city_state[0]
        state_name = city_state[1]

        event = Event.objects.create(name=name, organization=selected_org, loc_addr=addr,
                                     loc_city=city_name,
                                     loc_state=state_name,
                                     loc_zip=zip,
                                     time_happening=time_happening, description=description,
                                     time_published=time_published, image=photo)
        event.save()
        print("event saved?")

        interests = request.POST.getlist("selected_interests")
        for tag in interests:
            eventTag = EventTag.objects.create(event=event, interest=Interest.objects.get(tag=tag))
            eventTag.save()
            # should not get here
            if isinstance(eventTag, ValueError):
                check = Interest.objects.all()
                return render(request, "createevent.html",
                              {"message": 'Search Tag could not be applied', "interests": check})

        return render(request, "createevent.html", {'message': 'Event created successfully',
                                                    "orgs": orgs,
                                                    "user": current_user,
                                                    "interests": filtered_interests})