"""UWM_Clubs_and_Events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from UWM_Clubs_and_Events.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login.as_view(), name='login'),
    path('login/', Logout.as_view(), name='logout'),
    path("login.html", login.as_view()),
    path('homepage/', Homepage.as_view(), name='homepage'),
    path('homepage/', FilteredHomepage.as_view(), name='filteredhomepage'),
    path('createAccount/', CreateAccount.as_view(), name='createaccount'),
    path('viewevent<str:name>/', ViewEvent.as_view(), name='viewevent'),
    path('createAccount/', CreateAccount.as_view(), name='createaccount'),
    path('homepage/viewaccount/', ViewAccount.as_view(), name='viewaccount'),
    path('viewaccount/editaccount', EditAccount.as_view(), name='editaccount'),
    path('createOrganization/', CreateOrganization.as_view(), name='createorganization'),
    path('createEvent/', CreateEvent.as_view(), name='createevent'),

]
