from django.contrib import admin
from models import Jokes_jokes
from models import Jokes_funpics

# Register your models here.
admin.site.register(Jokes_jokes)
admin.site.register(Jokes_funpics)

list_display = ("content","preview")

def preview(self,obj):
    return '<img src="/static/%s" height="64" width="64" />' %(obj.photo)

preview.allow_tags = True
preview.short_description = "picture"
