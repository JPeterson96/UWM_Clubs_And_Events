from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class OrgPage(View):
    def get(self, request, name):
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        all_events = []
        curr_org = Organization.objects.get(name=name)

        if 'filters' not in request.session:
            all_events = Event.objects.filter(organization=curr_org)
        else:
            all_events = event_util.Event_Util.filter_events(
                user=current_user,
                sort_type=request.session['filters'][0],
                order=request.session['filters'][1],
                by_date=request.session['filters'][2],
                interests=None)
            all_events = all_events.filter(organization=curr_org)

        paginator = Paginator(all_events, 5)  # 5 events per page
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)
        return render(request, "orgpage.html", {"Events": events, "user": current_user, "curr_org": curr_org})

    def post(self, request, name):
        sort = request.POST.get('sortType')
        order = request.POST.get('sortOrder')
        date = request.POST.get('dateRange')
        clear = request.POST.get('clear')
        # interests = request.POST.getlist('interests')
        current_user = user_util.User_Util.get_user(email=request.session['user'])
        curr_org = Organization.objects.get(name=name)

        # convert to int
        sort = int(sort)
        order = int(order)
        date = int(date)

        filtered_events = event_util.Event_Util.filter_events(
            user=current_user,
            sort_type=sort,
            order=order,
            by_date=date,
            interests=None)
        filtered_events = filtered_events.filter(name=name)

        filters = []
        filters.append(sort)
        filters.append(order)
        filters.append(date)
        # filters.append(interests)
        request.session['filters'] = filters

        paginator = Paginator(filtered_events, 5)
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)

        return render(request, "orgpage.html", {"Events": events, "user": current_user, "curr_org": curr_org})