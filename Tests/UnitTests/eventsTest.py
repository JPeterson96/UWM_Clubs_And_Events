from django.test import TestCase
from django.test import Client

class test_getters(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event("name", "org","location","date","time","description", "event type", 1)

    def test_getName(self):
        self.assertEqual(self.event.getName(), "name")

    def test_getOrg(self):
        self.assertEqual(self.event.getOrg(), "org")

    def test_getLocation(self):
        self.assertEqual(self.event.getLocation(), "location")

    def test_getDate(self):
        self.assertEqual(self.event.getDate(), "date")

    def test_getTime(self):
        self.assertEqual(self.event.getTime(), "time")

    def test_getDescription(self):
        self.assertEqual(self.event.getDescription(), "description")

    def test_getEventType(self):
        self.assertEqual(self.event.getEventType(), "event type")

    def test_getViews(self):
        self.assertEqual(self.event.getViews(), 1)


class test_setters(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event()

    def test_setName(self):
        self.event.setName("name")
        self.assertEqual(self.event.getName(), "name")
    
    def test_setOrg(self):
        self.event.setOrg("org")
        self.assertEqual(self.event.getOrg(), "org")

    def test_setLocation(self):
        self.event.setLocation("location")
        self.assertEqual(self.event.getLocation(), "location")

    def test_setDate(self):
        self.event.setDate("date")
        self.assertEqual(self.event.getDate(), "date")

    def test_setTime(self):
        self.event.setTime("time")
        self.assertEqual(self.event.getTime(), "time")

    def test_setDescription(self):
        self.event.setDescription("description")
        self.assertEqual(self.event.getDescription(), "description")

    def test_setEventType(self):
        self.event.setEventType("event type")
        self.assertEqual(self.event.getEventType(), "event type")

    def test_setViews(self):
        self.event.setViews(1)
        self.assertEqual(self.event.getViews(), 1)
        