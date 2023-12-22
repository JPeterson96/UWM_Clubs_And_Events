from datetime import timedelta

from django.http import JsonResponse
from django.views import View

from UWM_Clubs_and_Events.models import *


class CalendarView(View):
    def get(self, request):
        all_events = Event.objects.all()

        all_events = Event.objects.all()
        event_list = []

        for event in all_events:
            event_list.append({
                'title': event.name,
                'start': event.time_happening.strftime("%Y-%m-%dT%H:%M:%S"),
                'end': (event.time_happening + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"),

            })

        """ 
        if not request.user.is_authenticated:
            return JsonResponse([], safe=False)


        user_attend_events = UserAttendEvent.objects.filter(user=request.user)
        print("RSVP'd Events: ", user_attend_events) # debuging print statments
        events = [event.event for event in user_attend_events]
        print("Events: ", events)
        print("Current user: ", request.user.email)

        event_list = []
        for user_attend_event in user_attend_events:
            event = user_attend_event.event
            event_data= {
                'title': event.name,
                'start': event.time_happening.strftime("%Y-%m-%dT%H:%M:%S"),
                'end': (event.time_happening + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"),    
            }

            print(event_data)  # Debugging line
            event_list.append(event_data)

            """

        return JsonResponse(event_list, safe=False)