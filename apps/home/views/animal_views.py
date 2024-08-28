# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from apps.home.services import animal_services
from apps.home.forms import animal_forms
from django.contrib import messages


@login_required(login_url="/login/")
def animals(request):

    if request.method == 'POST':
        print("executing post request")
        form = animal_forms.AddAnimalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print("form data: ", data)

            name = data['name']
            place_id = data['description']
            image = data['image']

            animal_services.add_animal(name, place_id, image)

            messages.success(request, 'Event created successfully')

            # return redirect('success')
    else:
        form = animal_forms.AddAnimalForm()

    animals_data = animal_services.get_animals_list()

    context = {
        'segment': 'events',
        'events': animals_data,
        'form': form,
    }

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))
