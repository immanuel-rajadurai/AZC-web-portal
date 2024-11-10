from django.urls import path, re_path

from .views import miscellaneous_views, animal_views, event_views, place_views, user_views

urlpatterns = [
    # home page
    path('', miscellaneous_views.index, name='home'),

    # animal views
    path('animals/', animal_views.all_animals, name='animals'),
    path('remove_animal/<str:animal_id>/',
         animal_views.remove_animal, name='remove_animal'),
    path('edit_animal/<str:animal_id>/',
         animal_views.edit_animal, name='edit_animal'),


    # event views
    path('events/', event_views.all_events, name='events'),
    path('delete_event/<str:event_id>',
         event_views.delete_event, name='delete_event'),
    path('edit_event/<str:event_id>/',
         event_views.edit_event, name='edit_event'),
    path('add_place_to_event/<str:place_id>/<str:event_id>',
         event_views.add_place_to_event, name='add_place_to_event'),
    path('remove_place_from_event/<str:place_id>/<str:event_id>',
         event_views.remove_place_from_event, name='remove_place_from_event'),


    # place views
    path('places/', place_views.all_places, name='places'),
    path('delete_place/<str:place_id>',
         place_views.delete_place, name='delete_place'),
    path('edit_place/<str:place_id>/',
         place_views.edit_place, name='edit_place'),
    path('add_animal_to_place/<str:animal_id>/<str:place_id>',
         place_views.add_animal_to_place, name='add_animal_to_place'),
    path('remove_animal_from_place/<str:animal_id>/<str:place_id>',
         place_views.remove_animal_from_place, name='remove_animal_from_place'),


    # user views
    path('users/', user_views.all_users, name='users'),


    # Matches any html file
    re_path(r'^.*\.*', miscellaneous_views.pages),
]
