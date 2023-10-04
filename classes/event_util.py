# name - string
# org - string
# location - string
# time - string
# description - string

# below is not set up yet
# background-image - image
# type - string
# views - int

from UWM_Clubs_and_Events.models import Event

class Event_Util():
    def create_event(name, org, location, time, description):
        try:
            event = Event(name=name, organization=org, location=location, time=time, description=description)
            event.save()
            return event
        except:
            return None

    def get_event(id):
        try:
            return Event.objects.get(id=id)
        except:
            return None
        
    def get_all_events():
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
            return Event.objects.contains(name=name)
        except:
            return None
