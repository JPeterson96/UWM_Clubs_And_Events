from UWM_Clubs_and_Events.models import *

class Data_Populate():

    def main(self):

        self.populate_data()

    # email, password, role, name
    # add a few more students/orgs
    # User(email='', password='', role=, name=''),
    def populate_data(self):
        users = User.objects.bulk_create(
            [
                User(email='student@uwm.edu', password='student', role=0, name='John Smith'),
                User(email='jpet@uwm.edu', password='jpet', role=0, name='Jamie Peterson'),
                User(email='ikra@uwm.edu', password='ikra', role=0, name='Ilya Kravtsov'),
                User(email='jbau@uwm.edu', password='jbau', role=0, name='Jeny Belen Herrera Bautista'),
                User(email='orma@uwm.edu', password='orma', role=0, name='Omar Abu-Rmaileh'),
                User(email='enie@uwm.edu', password='enie', role=0, name='Ethan Nieskes'),
                User(email='officer@uwm.edu', password='officer', role=1, name="Josh Rosh"),
                User(email='organization@uwm.edu', password='org', role=2, name='Fake Club'),
                User(email='computerclub@uwm.edu', password='compclub', role=2, name='Computer Club'),
                User(email='musicclub@uwm.edu', password='musicclub', role=2, name='Music Club'),
                User(email='faculty@uwm.edu', password='staff', role=3, name='Joe Teacher'),
                User(email='business@uwm.edu', password='business', role=3, name='Real Corp.'),

            ]
        )

        for user in users:
            user.save()

        # user, name, point_of_contact, memberCount, description
        # Organization(user=User.objects.get(email=''), name='', point_of_contact='', membersCount=),
        organizations = Organization.objects.bulk_create(
            [
                Organization(user=User.objects.get(email='organization@uwm.edu'), name='Fake Club',
                             point_of_contact='Joe Teacher', membersCount=12,
                             description='Fake Club is a club that isn\'t actually real.'),
                Organization(user=User.objects.get(email='computerclub@uwm.edu'), name='Computer Club',
                             point_of_contact='Joe Teacher', membersCount=5),
                Organization(user=User.objects.get(email='musicclub@uwm.edu'), name='Music Club',
                             point_of_contact='Joe Teacher', membersCount=2),
            ]
        )

        # add a few more here
        for org in organizations:
            org.save()

        # Student(user=User.objects.get(email='', enrollment_date=datetime.now(), graduation_date=None)),
        students = Student.objects.bulk_create(
            [
                Student(
                    user=User.objects.get(email='student@uwm.edu', enrollment_date=datetime.now(), graduate_date=None)),
                Student(
                    user=User.objects.get(email='jpet@uwm.edu', enrollment_date=datetime.now(), graduation_date=None)),
                Student(
                    user=User.objects.get(email='ikra@uwm.edu', enrollment_date=datetime.now(), graduation_date=None)),
                Student(
                    user=User.objects.get(email='jbau@uwm.edu', enrollment_date=datetime.now(), graduation_date=None)),
                Student(
                    user=User.objects.get(email='orha@uwm.edu', enrollment_date=datetime.now(), graduation_date=None)),
                Student(
                    user=User.objects.get(email='enie@uwm.edu', enrollment_date=datetime.now(), graduation_date=None)),
            ]
        )

        for student in students:
            student.save()

        majors = Major.objects.bulk_create(
            [
                Major(name="Computer Science", department="CEAS"),
                Major(name="Accounting", department="Finance"),
                Major(name="Biology", department="Science"),
                Major(name="Communications", department="English"),
                Major(name="Psychology", department="Science"),
                Major(name="Architecture", department="Design"),
                Major(name="History", department="History"),
                Major(name="Vocal Performance", department="Music"),
                Major(name="graphic design", department="Art"),
            ]
        )

        for major in majors:
            major.save()

        # StudentMajor(user=User.objects.get(email=''), major=Major.objects.get(name='')),
        student_majors = StudentMajor.objects.bulk_create(
            [
                StudentMajor(user=User.objects.get(email='student@uwm.edu'),
                             major=Major.objects.get(name='Accounting')),
                StudentMajor(user=User.objects.get(email='jpet@uwm.edu'),
                             major=Major.objects.get(name='Computer Science')),
                StudentMajor(user=User.objects.get(email='ikra@uwm.edu'),
                             major=Major.objects.get(name='Computer Science')),
                StudentMajor(user=User.objects.get(email='ohra@uwm.edu'),
                             major=Major.objects.get(name='Computer Science')),
                StudentMajor(user=User.objects.get(email='jbau@uwm.edu'),
                             major=Major.objects.get(name='Computer Science')),
                StudentMajor(user=User.objects.get(email='enie@uwm.edu'),
                             major=Major.objects.get(name='Computer Science')),
            ]
        )

        for stuMajor in student_majors:
            stuMajor.save()

        # diverse interests
        interests = Interest.objects.bulk_create(
            [
                Interest(tag="bowling"),
                Interest(tag="dance"),
                Interest(tag="music"),
                Interest(tag="art"),
                Interest(tag="business"),
                Interest(tag="Computer Science"),
                Interest(tag="Food"),
                Interest(tag="Pizza"),
                Interest(tag="Games"),
                Interest(tag="free"),
                Interest(tag="culture"),
                Interest(tag="Public"),
                Interest(tag="Alumni"),
                Interest(tag="Students"),
                Interest(tag="Sports"),
                Interest(tag="Football"),
                Interest(tag="Soccer"),
                Interest(tag="Tennis"),
                Interest(tag="Basketball"),
                Interest(tag="Health"),
                Interest(tag="Fitness"),
                Interest(tag="Learning"),
                Interest(tag="Advocacy"),
                Interest(tag="Rally"),
            ]
        )

        for interest in interests:
            interest.save()

        # StudentInterest(user=User.objects.get(email=""),type=Interest.objects.get(tag="")),
        studentInterests = StudentInterest.objects.bulk_create(
            [
                StudentInterest(user=User.objects.get(email="student@uwm.edu"),
                                type=Interest.objects.get(tag="Computer Science")),
                StudentInterest(user=User.objects.get(email="student@uwm.edu"),
                                type=Interest.objects.get(tag="bowling")),
                StudentInterest(user=User.objects.get(email="student@uwm.edu"), type=Interest.objects.get(tag="art")),
                StudentInterest(user=User.objects.get(email="jpet@uwm.edu"),
                                type=Interest.objects.get(tag="Computer Science")),
                StudentInterest(user=User.objects.get(email="jpet@uwm.edu"), type=Interest.objects.get(tag="Pizza")),
                StudentInterest(user=User.objects.get(email="ikra@uwm.edu"),
                                type=Interest.objects.get(tag="Computer Science")),
                StudentInterest(user=User.objects.get(email="jbau@uwm.edu"),
                                type=Interest.objects.get(tag="Computer Science")),
                StudentInterest(user=User.objects.get(email="ohra@uwm.edu"),
                                type=Interest.objects.get(tag="Computer Science")),
                StudentInterest(user=User.objects.get(email="enie@uwm.edu"),
                                type=Interest.objects.get(tag="Computer Science")),
            ]
        )

        for stuInt in studentInterests:
            stuInt.save()

        # this uses the default image in static
        # Event(name='', organization=Organization.objects.get(user=User.objects.get(email='')), location='', time_happening=datetime(Y, M, D, H, M, S, ms), description=''),
        events = Event.objects.bulk_create(
            [
                Event(name='Game Night',
                      organization=Organization.objects.get(user=User.objects.get(email='computerclub@uwm.edu')),
                      location='EMS120',
                      time_happening=datetime(2023, 11, 14, 18, 0, 0, 0), description='Relaxing Game Night in the EMS '
                                                                                      'Building'),
                Event(name='Fall Concert',
                      organization=Organization.objects.get(user=User.objects.get(email='musicclub@uwm.edu')),
                      location='Zelazo Performing Center',
                      time_happening=datetime(2023, 11, 28, 16, 0, 0, 0), description='The Fall Concert for the music '
                                                                                      'department'),
                Event(name='Bowling Night',
                      organization=Organization.objects.get(user=User.objects.get(email='fakeclub@uwm.edu')),
                      location='UREC',
                      time_happening=datetime(2023, 10, 12, 19, 0, 0, 0), description='Come for a fun night of '
                                                                                      'bowling in the Union\'s UREC '
                                                                                      'room'),
            ]
        )

        for event in events:
            event.save()

        # Event(event=Event.objects.get(name=''), interest=Interest.objects.get(tag='')),
        event_tags = EventTag.objects.bulk_create(
            [
                Event(event=Event.objects.get(name=''), interest=Interest.objects.get(tag='')),
            ]
        )