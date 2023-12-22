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
from UWM_Clubs_and_Events.views.accountCalendar import accountCalendar
from UWM_Clubs_and_Events.views.CalendarView import CalendarView
from UWM_Clubs_and_Events.views.ClearAllFilters import ClearAllFilters
from UWM_Clubs_and_Events.views.ClearFilters import ClearFilters
from UWM_Clubs_and_Events.views.CreateAccount import CreateAccount
from UWM_Clubs_and_Events.views.CreateEvent import CreateEvent
from UWM_Clubs_and_Events.views.CreateOrganization import CreateOrganization
from UWM_Clubs_and_Events.views.EditAccount import EditAccount
from UWM_Clubs_and_Events.views.EditEvent import EditEvent
from UWM_Clubs_and_Events.views.EditOrganization import EditOrganization
from UWM_Clubs_and_Events.views.Homepage import Homepage
from UWM_Clubs_and_Events.views.login import login
from UWM_Clubs_and_Events.views.Logout import Logout
from UWM_Clubs_and_Events.views.OrgPage import OrgPage
from UWM_Clubs_and_Events.views.ViewAccount import ViewAccount
from UWM_Clubs_and_Events.views.ViewEvent import ViewEvent
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import CalendarView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login.as_view(), name='login'),
    path('login/', Logout.as_view(), name='logout'),
    path("login.html", login.as_view()),
    path('homepage/', Homepage.as_view(), name='homepage'),
    path('homepage/filter', ClearFilters.as_view(), name='clearfilters'),
    path('homepage/all', ClearAllFilters.as_view(), name='clearallfilters'),
    path('createAccount/', CreateAccount.as_view(), name='createaccount'),
    path('viewevent/<int:id>/', ViewEvent.as_view(), name='viewevent'),
    path('createAccount/', CreateAccount.as_view(), name='createaccount'),
    path('homepage/viewaccount/', ViewAccount.as_view(), name='viewaccount'),
    path('viewaccount/editaccount', EditAccount.as_view(), name='editaccount'),
    path('createOrganization/', CreateOrganization.as_view(), name='createorganization'),
    path('createEvent/', CreateEvent.as_view(), name='createevent'),
    path('editOrganization/', EditOrganization.as_view(), name='editorganization'),
    path('editEvent/<int:id>/', EditEvent.as_view(), name='editevent'),
    path('calendar/', CalendarView.as_view(), name='publicEvents'),
    path('all_events/', CalendarView.as_view(), name='all_events'),
    path('homepage/accountCalendar/', accountCalendar.as_view(), name='accountCalendar'),
    path('orgpage/<str:name>/', OrgPage.as_view(), name='orgpage'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)