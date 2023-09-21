from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
