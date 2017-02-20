from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Face_main(models.Model):
    image = models.ImageField()
    predicted_age = models.CharField(max_length=5)
    # predicted_gender = models.CharField(max_length=10)
    # predicted_glass = models.CharField(max_length=10)
    # predicted_smile = models.CharField(max_length=25)
    # dateTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.image
