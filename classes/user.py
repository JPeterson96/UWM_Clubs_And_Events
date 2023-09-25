def User(self):
    name = ""
    email = ""
    password = ""
    role = 0
    interests = []
    orgs = []
    major = ""
    friends = []

    def __init__(self, name, email, password, role, interests, org_tags, major, friends):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.interests = interests
        self.orgs = org_tags
        self.major = major
        self.friends = friends

    def getName(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getPassword(self):
        return self.password
    
    def getRole(self):
        return self.role
    
    def getInterests(self):
        return self.interests
    
    def getOrgs(self):
        return self.org_tags
    
    def getMajor(self):
        return self.major
    
    def getFriends(self):
        return self.friends
    
    def setName(self, name):
        self.name = name

    def setEmail(self, email):
        self.email = email

    def setPassword(self, password):
        self.password = password

    def setRole(self, role):
        self.role = role

    def setInterests(self, interests):
        self.interests = interests

    def setOrgs(self, org_tags):
        self.org_tags = org_tags

    def setMajor(self, major):
        self.major = major

    def setFriends(self, friends):
        self.friends = friends
