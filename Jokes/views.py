# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from models import Jokes_jokes
from models import Jokes_funpics
from serializers import JokesSerializer
from serializers import FunpicsSerializer
from rest_framework import viewsets

class JokesViewSet(viewsets.ModelViewSet):
    queryset = Jokes_jokes.objects.all()
    serializer_class = JokesSerializer

class FunpicsViewSet(viewsets.ModelViewSet):
    queryset = Jokes_funpics.objects.all()
    serializer_class = FunpicsSerializer

from rest_framework import generics


class JokesList(generics.ListCreateAPIView):
    queryset = Jokes_jokes.objects.all()
    serializer_class = JokesSerializer


class JokesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jokes_jokes.objects.all()
    serializer_class = JokesSerializer

