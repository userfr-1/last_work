from django.db import models

from . import Organization


#from configApp.models import Organization, GroupTech


from ..models import *


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.full_name

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_activate = models.BooleanField(default=False)
    group = models.ManyToManyField("Group",related_name='group')
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.full_name
