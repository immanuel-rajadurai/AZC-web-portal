# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path, re_path

from apps.home.views import animal_views, event_views, miscellaneous_views, place_views

urlpatterns = [
    # The home page
    path('', miscellaneous_views.index, name='home'),

    path('events/', event_views.all_events, name='events'),
    path('delete_event/<str:event_id>/', event_views.delete_event, name='delete_event'),
    path('places/', place_views.all_places, name='places'),
    path('animals/', animal_views.all_animals, name='animals'),

    # Matches any html file
    re_path(r'^.*\.*', miscellaneous_views.pages, name='pages'),
]
