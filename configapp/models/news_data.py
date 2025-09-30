from django.db import models

class NewsFotos(models.Model):
    title = models.CharField(max_length=500)
    image = models.URLField()

class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    count = models.IntegerField(default=0)
    images = models.ManyToManyField(NewsFotos, related_name="images")
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title