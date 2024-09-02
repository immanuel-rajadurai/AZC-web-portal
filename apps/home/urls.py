# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path, re_path

from apps.home.views import animal_views, event_views, miscellaneous_views, place_views

urlpatterns = [
    # The home page
    path('', miscellaneous_views.index, name='home'),


    path('events/', event_views.events, name='events'),
    path('places/', place_views.places, name='places'),
    path('animals/', animal_views.animals, name='animals'),

    # Matches any html file
    re_path(r'^.*\.*', miscellaneous_views.pages, name='pages'),
]
