# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path, re_path

from .views import miscellaneous_views, animal_views, event_views, place_views

urlpatterns = [
    # The home page
    path('', miscellaneous_views.index, name='home'),


    path('animals/', animal_views.all_animals, name='animals'),
    path('delete_animal/<str:event_id>/',
         animal_views.remove_animal, name='delete_animal'),

    path('events/', event_views.all_events, name='events'),
    path('delete_event/<str:event_id>/',
         event_views.delete_event, name='delete_event'),

    path('places/', place_views.all_places, name='places'),
    path('delete_place/<str:event_id>/',
         place_views.delete_place, name='delete_place'),


    # Matches any html file
    re_path(r'^.*\.*', miscellaneous_views.pages),
]