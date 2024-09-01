# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from ..services import animal_services
from ..forms import animal_forms


@login_required(login_url="/login/")
def all_animals(request):
    if request.method == 'POST':
        print("executing post request")
        form = animal_forms.AddAnimalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print("form data: ", data)

            name = data['name']
            image = data['image']

            animal_services.add_animal(name, image)

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
