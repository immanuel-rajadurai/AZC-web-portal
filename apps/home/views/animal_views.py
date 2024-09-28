# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import messages

from ..services import animal_services
from ..forms import animal_forms


@login_required(login_url="/login/")
def all_animals(request):
    if request.method == 'POST':
        # print("executing post request")
        form = animal_forms.AnimalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            image = data['image']

            animal_services.add_animal(name, image)

            messages.success(request, 'Animal created successfully')
    else:
        form = animal_forms.AnimalForm()

    context = {
        'segment': 'animals',
        'animals': animal_services.get_animals_list(),
        'form': form,
    }

    html_template = loader.get_template('home/show_animals.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def remove_animal(request, animal_id):
    # print("attempting to remove animal ", animal_id)
    animal_services.remove_animal(animal_id)

    messages.success(request, 'Animal removed successfully')
    return redirect('animals')


@login_required(login_url="/login/")
def edit_animal(request, animal_id):
    animal = animal_services.get_animal(animal_id)\

    # print(request.method)

    if request.method == 'POST':
        # print("executing post request")
        form = animal_forms.AnimalForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            image = data['image']

            animal_services.edit_animal(animal_id, name, image)

            return redirect('animals')
    else:
        form = animal_forms.AnimalForm()

        form.fields['name'].initial = animal['name']
        form.fields['image'].initial = animal['image']

    context = {
        'segment': 'animals',
        'animal': animal,
        'form': form,
    }

    html_template = loader.get_template('home/edit_animal.html')
    return HttpResponse(html_template.render(context, request))
