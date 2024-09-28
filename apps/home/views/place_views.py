# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import messages
from ..services import animal_services, place_services, animal_place_services
from ..forms import place_forms


@login_required(login_url="/login/")
def all_places(request):
    if request.method == 'POST':
        print("executing post request")
        form = place_forms.PlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("form data: ", data)

            name = data['name']
            description = data['description']
            isOpen = data['isOpen']
            image = data['image']

            place_services.create_place(
                name, description, isOpen, image)

            messages.success(request, 'Place created successfully')
    else:
        form = place_forms.PlaceForm()

    context = {
        'segment': 'places',
        'places': place_services.get_places_list(),
        'animals': animal_services.get_animals_list(),
        'form': form,
    }

    html_template = loader.get_template('home/show_places.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_place(request, place_id):
    # print("attempting to delete place: ", place_id)
    place_services.delete_place(place_id)

    messages.success(request, 'Place deleted successfully')
    return redirect('places')


@login_required(login_url="/login/")
def add_animal_to_place(request, place_id, animal_id):
    # print("attemping to add animal to place")

    animal_place_services.add_animal_to_place(place_id, animal_id)

    messages.success(request, 'Animal assigned successfully')
    return redirect('places')


@login_required(login_url="/login/")
def edit_place(request, place_id):
    place = place_services.get_place(place_id)

    if request.method == 'POST':
        # print("executing post request")
        form = place_forms.PlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print("place form data: ", data)


            name = data['name']
            description = data['description']
            isOpen = data['isOpen']
            image = data['image']

            place_services.edit_place(place_id, name, description, isOpen, image)

            messages.success(request, f""""{name}" edited successfully""")

            return redirect('places')
    else:
        form = place_forms.PlaceForm()

        form.fields['name'].initial = place['name']
        form.fields['description'].initial = place['description']
        form.fields['isOpen'].initial = place['isOpen']
        form.fields['image'].initial = place['image']

    context = {
        'segment': 'animals',
        'place': place,
        'form': form,
    }

    html_template = loader.get_template('home/edit_place.html')
    return HttpResponse(html_template.render(context, request))
