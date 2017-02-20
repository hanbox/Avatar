# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

from . import views
from models import Jokes_jokes
from models import Jokes_funpics
from rest_framework import routers, serializers, viewsets

class JokesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Jokes_jokes
        fields = ('title', 'data', 'src_url', 'dateTime')

class JokesViewSet(viewsets.ModelViewSet):
    queryset = Jokes_jokes.objects.all()
    serializer_class = JokesSerializer

class FunpicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Jokes_funpics
        fields = ('title', 'image_paths', 'src_url', 'dateTime')

class FunpicsViewSet(viewsets.ModelViewSet):
    queryset = Jokes_funpics.objects.all()
    serializer_class = FunpicsSerializer

def regRouter(router):
    router.register(r'jokes', JokesViewSet)
    router.register(r'funpics', FunpicsViewSet)

