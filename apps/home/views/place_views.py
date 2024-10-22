from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import messages

from ..services import animal_services, place_services, animal_place_services
from ..forms import place_forms
from .miscellaneous_views import get_ids_from_filter


@login_required(login_url="/login/")
def all_places(request):
    if request.method == 'POST':
        # print("executing post request")
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

    form = place_forms.PlaceForm()

    places = place_services.get_places_list()
    linked_animals = {}
    for place in places:
        tmp = animal_place_services.get_animals_linked_to_place(place['id'])
        tmp = get_ids_from_filter(tmp, "animalID")
        linked_animals.update({place['id']: tmp})

    # print("linked_animals: ", linked_animals)

    context = {
        'segment': 'places',
        'places': places,
        'linked_animals': linked_animals,
        'form': form,
    }

    html_template = loader.get_template('home/show_places.html')
    return HttpResponse(html_template.render(context, request))


@ login_required(login_url="/login/")
def delete_place(request, place_id):
    # print("attempting to delete place: ", place_id)
    place_services.delete_place(place_id)

    messages.success(request, 'Place deleted successfully')
    return redirect('places')


@ login_required(login_url="/login/")
def add_animal_to_place(request, animal_id, place_id):
    # print("attemping to add animal to place")

    animal_place_services.add_animal_to_place(animal_id, place_id)

    messages.success(request, 'Animal assigned successfully')
    return redirect('places')


@ login_required(login_url="/login/")
def edit_place(request, place_id):
    place = place_services.get_place(place_id)
    # print("place: ", place)

    if request.method == 'POST':
        # print("executing post request")
        form = place_forms.PlaceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # print("place_form data: ", data)

            name = data['name']
            description = data['description']
            isOpen = data['isOpen']
            image = data['image']

            place_services.edit_place(
                place_id, name, description, isOpen, image)

            messages.success(request, f""""{name}" edited successfully""")

            return redirect('places')
    else:
        form = place_forms.PlaceForm()
        form.fields['name'].initial = place['name']
        form.fields['description'].initial = place['description']
        form.fields['isOpen'].initial = place['isOpen']
        form.fields['image'].initial = place['image']

    linked_animals = animal_place_services.get_animals_linked_to_place(
        place_id)
    linked_animals = get_ids_from_filter(linked_animals, "animalID")
    # print("linked_animals: ", linked_animals)

    all_animals = animal_services.get_animals_list()
    # print("all_animals",  all_animals)
    animals = []
    for item in all_animals:
        # print("item['id']", item['id'])
        if not item['id'] in linked_animals:
            animals.append(item)

    # print("animals", animals)

    context = {
        'segment': 'places',
        'place': place,
        'place_id': place_id,
        'animals': animals,
        'linked_animals': linked_animals,
        'form': form,
    }

    html_template = loader.get_template('home/edit_place.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def remove_animal_from_place(request, animal_id, place_id):
    # print("attempting to delete event: ", event_id)
    animal_place_services.remove_animal_from_place(animal_id, place_id)

    messages.success(request, 'Animal detached successfully')
    return redirect('places')
