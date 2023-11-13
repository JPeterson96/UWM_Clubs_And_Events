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
    # sort_type - small int (0 = not applied, 1 = date, 2 = org_name, 3 = event_name)
    # order - small int (0 = not applied, 1 = ascending, 2 = descending)
    # by_date - small int (0 = not applied, 1 = today, 2 = tomorrow, 3 = this week, 4 = this month, 5 = this year)
    # clear - boolean
    # interests - list of Interest tags
    def filter_events(user, sort_type, order, by_date, clear, interests):
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
        if sort_type == 1:
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
        if sort_type == 1:
            if order == 1:
                filters.append("time_happening")
            elif order == 2:
                filters.append("-time_happening")

        if sort_type == 2:
            if order == 1:
                filters.append("organization__name")
            elif order == 2:
                filters.append("-organization__name")

        if sort_type == 3:
            if order == 1:
                filters.append("name")
            elif order == 2:
                filters.append("-name")

        filtered_events = filtered_events.order_by(*filters)

        return filtered_events

    # def verify_event_loc(addr, city, state, zip):
    #     if addr is None:
    #         return ValueError("address cannot be empty")
    #     if city is None:
    #         return ValueError("city cannot be empty")
    #     if state is None:
    #         return ValueError("state cannot be empty")
    #     if zip is None:
    #         return ValueError("zip cannot be empty")
    #     returntype = "locations"
    #     searchtype = "address"
    #     benchmark = "Public_AR_Current"
    #     format_type = "json"
    #     api_url = f"https://geocoding.geo.census.gov/geocoder/{returntype}/{searchtype}?benchmark={benchmark}&format={format_type}&street={addr}&city={city}&state={state}&zip={zip}"
    #     try:
    #         result = requests.get(api_url)
    #         if result.status_code==200:
    #             res_data = result.json()
    #             res_address = res_data['result']['addressMatches'][0]['matchedAddress']
    #             if res_address is None:
    #                 return ValueError("address inputted does not match")
    #
    #             # for now I will just change the event with input
    #
    #             #should display this address to user when checking
    #             print(res_address)
    #             return res_address
    #
    #     except requests.exceptions.HTTPError as e:
    #         return f"error with http request {e}"
    #     except requests.exceptions.RequestException as e:
    #         return f"error with  argument in http request, most likley a name of  addr, state, zip, or city  {e}"
    #     except Exception as e:
    #         print(f"Unexpected error occurred: {e}")

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
