# event - string
# name - string
# org - string
# location - string
# date - string
# time - string
# description - string
# background-image - image
# type - string
# views - int

class Event(object):
    event = ""
    name = ""
    org = ""
    location = ""
    date = ""
    time = ""
    description = ""
    background_image = None
    type = ""
    views = 0

    def __init__(self, event, name, org, location, date, time, description, background_image, type, views):
        self.event = event
        self.name = name
        self.org = org
        self.location = location
        self.date = date
        self.time = time
        self.description = description
        self.background_image = background_image
        self.type = type
        self.views = views

    def getEvent(self):
        return self.event
    
    def getName(self):
        return self.name
    
    def getOrg(self):
        return self.org
    
    def getLocation(self):
        return self.location
    
    def getDate(self):
        return self.date
    
    def getTime(self):
        return self.time
    
    def getDescription(self):
        return self.description
    
    def getBackgroundImage(self):
        return self.background_image
    
    def getType(self):
        return self.type

    def getViews(self):
        return self.views
    
    def setEvent(self, event):
        self.event = event

    def setName(self, name):
        self.name = name

    def setOrg(self, org):
        self.org = org

    def setLocation(self, location):
        self.location = location

    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time

    def setDescription(self, description):
        self.description = description

    def setBackgroundImage(self, background_image):
        self.background_image = background_image

    def setType(self, type):
        self.type = type

    def setViews(self, views):
        self.views = views
