# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from ..services import event_services, place_services
from ..forms import event_forms


@login_required(login_url="/login/")
def all_events(request):
    if request.method == 'POST':
        print("executing post request")
        form = event_forms.CreateEventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            description = data['description']
            # place_id = data['place_id']
            image = data['image']

            # event_services.create_event(
            #     name, description, place_id, image)

            event_services.create_event(name, description, image)

            messages.success(request, 'Event created successfully')

    else:
        form = event_forms.CreateEventForm()

    context = {
        'segment': 'events',
        # 'events': {},
        'events': event_services.get_events_list(),
        # 'places': {},
        'places': place_services.get_places_list(),
        'form': form,
    }

    html_template = loader.get_template('home/show_events.html')

    # print("HTML template ", html_template)

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_event(request, event_id):
    print("attempting to delete event: ", event_id)
    event_services.delete_event(event_id)

    messages.success(request, 'Event deleted successfully')
    return redirect('events')
