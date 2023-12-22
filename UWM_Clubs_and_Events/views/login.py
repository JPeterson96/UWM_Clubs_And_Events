from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UWM_Clubs_and_Events.models import *
from classes import user_util, event_util, organization_util
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta

class login(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html', {"name": "login"})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.get(email=request.POST.get('email'))
            badPassword = (user.password != request.POST.get('password'))
        except:
            noSuchUser = True
        if email == '' and password == '':
            return render(request, "login.html", {"message": "Nothing entered"})
        elif email == '':
            return render(request, "login.html", {"message": "No email"})
        elif password == '':
            return render(request, "login.html", {"message": "no password"})
        elif noSuchUser:
            return render(request, "login.html", {"message": "no user in database"})
        elif badPassword:
            return render(request, "login.html", {"message": "no user with this password"})
        else:
            request.session['user'] = user.email
            return redirect("homepage")