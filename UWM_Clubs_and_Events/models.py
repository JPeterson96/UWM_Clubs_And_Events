from datetime import datetime

from django.db import models


# Model Fields: EmailField, CharField, IntegerField
# models.TextChoices
# to_field argument in Models.ForeignKey()

# name-str, email-str, password-str, role-?, interests/tags-?, orgs-?, majors-?, friends-?
# can edit:  Interest, Major, Graduation Date,
class User(models.Model):
    email = models.EmailField(max_length=30, unique=True)  # add email validator?
    password = models.CharField(max_length=30)
    role = models.PositiveSmallIntegerField(
        choices=((0, "Student"), (1, "Student Club Contact"), (2, "Organization"), (3, "Point of Contact")), default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    enrollment_date = models.DateField(null=True, editable=False)
    graduation_date = models.DateField(null=True)

    def __str__(self):
        return self.user.email


# # Org/Club:  name-str, point_of_contact-str/email, membersCount-int, description-str, staff-User(staff to anchor),
# majors-?
class Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    point_of_contact = models.CharField(max_length=30)
    membersCount = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Events:  name-str, organization-str, location-str, date-str/Date/Time, description-str, type-str, views-int
class Event(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='name')
    location = models.CharField(max_length=30)
    # this uses a YYYY-MM-DD for the date, and HH:MM:SS for the time
    time_happening = models.DateTimeField()  # look into these 2 fields some more
    description = models.TextField()
    time_published = models.DateTimeField(null=True)
    # if a user doesn't upload an image there will be a default image
    image = models.ImageField(upload_to='static/event_photos', default='static/event_photos/default.jpeg')

    # image here/file path for image?  where do we store/upload
    def __str__(self):
        return self.name + "/" + self.organization.name

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(Event, self).delete(*args, **kwargs)


class MembersIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return self.user.email + "/" + self.organization.name


class Major(models.Model):
    # consider using choices here for these?
    name = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=20)

    def __str__(self):
        return self.name + "/" + self.department


class Interest(models.Model):
    tag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Interest, on_delete=models.CASCADE, to_field='tag')

    def __str__(self):
        return self.user.email + "/" + self.type.tag


class StudentInterest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.ForeignKey(Interest, on_delete=models.CASCADE, to_field='tag')

    def __str__(self):
        return self.student.user.email + "/" + self.type.tag


class EventTag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, to_field='tag')

    def __str__(self):
        return self.event.name + "/" + self.interest.tag


class StudentMajor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return self.student.user.email + "/" + self.major.name

# class Friend(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
#     friend_with = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
#
#     def __str__(self):
#         return self.user.email + "/" + self.friend_with.email

# class PendingFriends(models.Model):
#     user_requester = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
#     user_requested = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
#
#     def __str__(self):
#         return "User " + self.user_requester.email + " sent user " + self.user_requested.email + " a friend request."

class Calendar(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 
    class Meta:  
        db_table = "tblevents"
        
        
    
