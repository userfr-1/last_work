from django.db import models
from .auth_user import User


class Region(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class Organization(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class ManagerOrganization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.username