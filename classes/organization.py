# name
# point_of_contact
# members
# description
# role
# interests

def Organization(self):
    name = ""
    point_of_contact = ""
    members = []
    description = ""
    role = []
    interests = []

    def __init__(self, name, point_of_contact, members, description, role, interests):
        self.name = name
        self.point_of_contact = point_of_contact
        self.members = members
        self.description = description
        self.role = role
        self.interests = interests

    def getName(self):
        return self.name
    
    def getPointOfContact(self):
        return self.point_of_contact
    
    def getMembers(self):
        return self.members
    
    def getDescription(self):
        return self.description
    
    def getRole(self):
        return self.role
    
    def getInterests(self):
        return self.interests
    
    def setName(self, name):
        self.name = name

    def setPointOfContact(self, point_of_contact):
        self.point_of_contact = point_of_contact

    def setMembers(self, members):
        self.members = members

    def setDescription(self, description):
        self.description = description

    def setRole(self, role):
        self.role = role

    def setInterests(self, interests):
        self.interests = interests