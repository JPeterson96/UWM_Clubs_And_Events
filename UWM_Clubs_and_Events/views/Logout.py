from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class Logout(View):
    def get(self, request):
        try:
            logout(request)
        except KeyError:
            pass
        return redirect("login")