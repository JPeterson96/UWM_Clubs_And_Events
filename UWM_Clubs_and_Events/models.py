from django.db import models


# Model Fields: EmailField, CharField, IntegerField
# models.TextChoices
# to_field argument in Models.ForeignKey()

# name-str, email-str, password-str, role-?, interests/tags-?, orgs-?, majors-?, friends-?
class User(models.Model):
    email = models.EmailField(max_length=30)  # add email validator?
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Events:  name-str, organization-str, location-str, date-str/Date/Time, description-str, type-str, views-int
class Events(models.Model):
    name = models.CharField(max_length=30)
    organization = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    time = models.DateTimeField()
    description = models.TextField()

    # image here/file path for image?  where do we store/upload
    def __str__(self):
        return self.name + "/" + self.organization


# Org/Club:  name-str, point_of_contact-str/email, membersCount-int, description-str, staff-User(staff to anchor), majors-?
class Organizations(models.Model):
    name = models.CharField(max_length=20)
#    point_of_contact = models.ForeignKey(User)
    membersCount = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MembersIn(models.Model):
   # user = models.ForeignKey(User)
    #name = models.ForeignKey(Organizations)

    def __str__(self):
        return self.user + "/" + self.name


class Majors(models.Model):
    # consider using choices here for these?
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=20)

    def __str__(self):
        return self.name + "/" + self.department


class Interests(models.Model):
    type = models.CharField(max_length=15)

    def __str__(self):
        return self.name

# check how cascade actually works
# class UserInterests(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    type = models.ForeignKey(Interests, on delete=models.CASCADE)
