# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import include, url

from views import JokesViewSet
from views import FunpicsViewSet

def regRouter(router):
    router.register(r'jokes', JokesViewSet)
    router.register(r'funpics', FunpicsViewSet)

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^jokes/$', views.JokesList.as_view()),
    url(r'^jokes/(?P<pk>[0-9]+)/$', views.JokesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)