# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import messages

from ..services import event_services, place_event_services, place_services
from ..forms import event_forms


@login_required(login_url="/login/")
def all_events(request):
    if request.method == 'POST':
        # print("executing post request")
        form = event_forms.EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            description = data['description']
            image = data['image']

            event_services.create_event(name, description, image)

            messages.success(request, 'Event created successfully')
    else:
        form = event_forms.EventForm()

    events = event_services.get_events_list()
    linked_places = {}
    for event in events:
        tmp = place_event_services.get_places_linked_to_event(event['id'])
        linked_places.update({event['id']: tmp})

    # print("linked_places: ", linked_places)

    context = {
        'segment': 'events',
        'events': events,
        'linked_places': linked_places,
        'form': form,
    }

    html_template = loader.get_template('home/show_events.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_event(request, event_id):
    # print("attempting to delete event: ", event_id)
    event_services.delete_event(event_id)

    messages.success(request, 'Event deleted successfully')
    return redirect('events')


@login_required(login_url="/login/")
def add_place_to_event(request, place_id, event_id):
    # print("attemping to add place to event")

    place_event_services.add_place_to_event(event_id, place_id)

    messages.success(request, 'Place assigned successfully')
    return redirect('events')


@login_required(login_url="/login/")
def edit_event(request, event_id):
    event = event_services.get_event(event_id)
    print(event)

    if request.method == 'POST':
        # print("executing post request")
        form = event_forms.EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            description = data['description']
            image = data['image']

            event_services.edit_event(event_id, name, description, image)

            messages.success(request, f""""{name}" edited successfully""")

            return redirect('events')
    else:
        form = event_forms.EventForm()
        form.fields['name'].initial = event['name']
        form.fields['description'].initial = event['description']
        form.fields['image'].initial = event['image']

    tmp = place_event_services.get_places_linked_to_event(
        event_id)
    linked_places = []
    if tmp:
        linked_places = list(tmp.values())
        # print("linked_places: ", linked_places)

    context = {
        'segment': 'animals',
        'event': event,
        'event_id': event_id,
        'all_places': place_services.get_places_list(),
        'linked_places': linked_places,
        'form': form,
    }

    html_template = loader.get_template('home/edit_event.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def remove_place_from_event(request, place_id, event_id):
    # print("attempting to delete event: ", event_id)
    place_event_services.remove_place_from_event(place_id, event_id)

    messages.success(request, 'Place detached successfully')
    return redirect('events')
