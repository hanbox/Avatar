from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Speech_main(models.Model):
    data = models.CharField(max_length=255)
    sentiments = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
    	return self.data