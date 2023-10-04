from django.db import models


# Model Fields: EmailField, CharField, IntegerField
# models.TextChoices
# to_field argument in Models.ForeignKey()

# name-str, email-str, password-str, role-?, interests/tags-?, orgs-?, majors-?, friends-?
class User(models.Model):
    email = models.EmailField(max_length=30, unique=True)  # add email validator?
    password = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    role = models.PositiveSmallIntegerField(choices=((0, "Student"), (1, "Organization")), default=0)

    def __str__(self):
        return self.name


# # Org/Club:  name-str, point_of_contact-str/email, membersCount-int, description-str, staff-User(staff to anchor), majors-?
# class Organization(models.Model):
#     name = models.CharField(max_length=20, unique=True)
#     point_of_contact = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
#     membersCount = models.IntegerField()
#     description = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name


# Events:  name-str, organization-str, location-str, date-str/Date/Time, description-str, type-str, views-int
class Event(models.Model):
    name = models.CharField(max_length=30, unique=True)
    organization = models.CharField(max_length=30)  # foreign key this?
    location = models.CharField(max_length=30)
    # this uses a YYYY-MM-DD for the date, and HH:MM:SS for the time
    time = models.DateTimeField()  # look into these 2 fields some more
    description = models.TextField()

    # image here/file path for image?  where do we store/upload
    def __str__(self):
        return self.name + "/" + self.organization


# class MembersIn(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
#     name = models.ForeignKey(Organizations, on_delete=models.CASCADE, to_field='name')
#
#     def __str__(self):
#         return self.user + "/" + self.name
#
#
class Major(models.Model):
    # consider using choices here for these?
    name = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name + "/" + self.department


class UserMajor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    major = models.ForeignKey(Major, on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return self.user + "/" + self.major


class Interest(models.Model):
    tag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag


# check how cascade actually works
class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    type = models.ForeignKey(Interest, on_delete=models.CASCADE, to_field='tag')

    def __str__(self):
        return self.user.email + "/" + self.type.tag


class EventTag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, to_field='name')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, to_field='tag')

    def __str__(self):
        return self.event.name + "/" + self.interest.tag
