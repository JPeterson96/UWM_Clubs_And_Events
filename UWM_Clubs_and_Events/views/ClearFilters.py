from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class ClearFilters(View):
    def get(self, request):
        if 'filters' in request.session:
            del request.session['filters']

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        user_interests = StudentInterest.objects.filter(student__user=current_user)
        interest_tags = [interest.type.tag for interest in user_interests]

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        all_events = event_util.Event_Util.filter_events(
            user=current_user,
            sort_type=0,
            order=0,
            by_date=0,
            interests=interest_tags)

        paginator = Paginator(all_events, 5)
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)

        return render(request, "homepage.html", {"Events": events, "user": current_user})