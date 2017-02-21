from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Jokes_jokes(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    data = models.CharField(max_length=255)
    src_url = models.CharField(max_length=150)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class Jokes_funpics(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    image_paths = models.ImageField()
    src_url = models.CharField(max_length=150)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title