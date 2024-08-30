# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from apps.home.services import event_services
from apps.home.forms import event_forms
from django.contrib import messages


@login_required(login_url="/login/")
def all_events(request):

    if request.method == 'POST':
        print("executing post request")
        form = event_forms.CreateEventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print("form data: ", data)

            name = data['name']
            description = data['description']
            place_id = data['place_id']
            animal_id = data['animal_id']
            image = data['image']

            event_services.create_event(
                name, description, place_id, animal_id, image)

            messages.success(request, 'Event created successfully')

            # return redirect('success')
    else:
        form = event_forms.CreateEventForm()

    events_data = event_services.get_events_list()

    context = {
        'segment': 'events',
        'events': events_data,
        'form': form,
    }

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))
