# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from ..services import place_services
from ..forms import place_forms


@login_required(login_url="/login/")
def all_places(request):
    if request.method == 'POST':
        print("executing post request")
        form = place_forms.AddPlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            description = data['description']
            animal_id = data['animal_id']
            isOpen = data['isOpen']
            image = data['image']

            place_services.create_place(
                name, description, animal_id, isOpen, image)

            messages.success(request, 'Event created successfully')

            # return redirect('success')
    else:
        form = place_forms.AddPlaceForm()

    places_data = place_services.get_places_list()

    context = {
        'segment': 'events',
        'events': places_data,
        'form': form,
    }

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))
