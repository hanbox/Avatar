# -*- coding: utf-8 -*-
from models import Jokes_jokes
from models import Jokes_funpics
from rest_framework import serializers

class JokesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Jokes_jokes
        fields = ('id', 'title', 'data', 'src_url', 'dateTime')

class FunpicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Jokes_funpics
        fields = ('id', 'title', 'image_paths', 'src_url', 'dateTime')