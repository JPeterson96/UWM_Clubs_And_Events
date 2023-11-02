# name - string
# org - string
# location - string
# time - string
# description - string

# below is not set up yet
# type - string
# views - int

from UWM_Clubs_and_Events.models import Event
from datetime import datetime, timedelta
from django.db.models import Q


class Event_Util():
    def create_event(name, org, location, time, description):
        try:
            event = Event(name=name, organization=org, location=location, time=time, description=description)
            event.save()
            return True
        except Exception as e:
            print(e)
            return False

    # user - User object
    # by_date - small int (0 = not applied, 1 = today, 2 = tomorrow, 3 = this week, 4 = this month, 5 = this year)
    # date_order - small int (0 = not applied, 1 = ascending, 2 = descending)
    # by_org_name - small int (0 = not applied, 1 = ascending, 2 = descending)
    # by_event_name - small int (0 = not applied, 1 = ascending, 2 = descending)
    # clear - boolean
    # interests - list of Interest tags
    def filter_events(user, by_date, date_order, by_org_name, by_event_name, clear, interests):
        if clear:
            return list(Event.objects.all())

        # filtered_events = Event.objects.all()

        if interests:
            # Filter by interests
            query = Q()
            for i in interests:
                query |= Q(interests__name=i)
            filtered_events = Event.objects.filter(query).distinct()
        else:
            filtered_events = Event.objects.all()

        # Filter by date
        if by_date != 0:
            today = datetime.today()

            if by_date == 1:
                filtered_events = filtered_events.filter(time_happening__date=today)

            elif by_date == 2:
                filtered_events = filtered_events.filter(time_happening__date=today + timedelta(days=1))

            elif by_date == 3:
                filtered_events = filtered_events.filter(
                    time_happening__date__range=[today, today + timedelta(days=7)])

            elif by_date == 4:
                filtered_events = filtered_events.filter(
                    time_happening__date__range=[today, today + timedelta(days=30)])

            elif by_date == 5:
                filtered_events = filtered_events.filter(
                    time_happening__date__range=[today, today + timedelta(days=365)])

        filters = []
        # Sort events
        if date_order == 1:
            filters.append("time_happening")
        elif date_order == 2:
            filters.append("-time_happening")

        if by_org_name == 1:
            filters.append("organization__name")
        elif by_org_name == 2:
            filters.append("-organization__name")

        if by_event_name == 1:
            filters.append("name")
        elif by_event_name == 2:
            filters.append("-name")

        filtered_events = filtered_events.order_by(*filters)

        return filtered_events

    def get_event(id):
        try:
            return Event.objects.get(id=id)
        except:
            return None

    def get_all_events(self):
        try:
            return Event.objects.all()
        except:
            return None

    def get_org_events(org):
        try:
            return Event.objects.filter(organization=org)
        except:
            return None

    def get_event_by_name(name):
        try:
            return Event.objects.filter(name=name)
        except:
            return None
