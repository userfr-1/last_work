from django.db import models

class About(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Serves(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title