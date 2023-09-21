from django.views import View
from django.shortcuts import render

class login(View):
    def get(self, request):
        return render(request, 'login.html', {"name": "login"})