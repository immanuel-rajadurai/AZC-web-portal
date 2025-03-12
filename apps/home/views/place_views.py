from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from ..services import animal_services, place_services, animal_place_services
from ..forms import place_forms


@login_required(login_url="/login/")
def all_places(request):
    if request.method == "POST":
        form = place_forms.PlaceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            isOpen = form.cleaned_data["isOpen"]
            image = form.cleaned_data["image"]
            place_services.create_place(name, description, isOpen, image)

            messages.success(request, "Place created successfully")

        else:
             messages.error(request, "Place not created, check formatting")

    form = place_forms.PlaceForm()

    all_places = place_services.get_places_list()
    linked_animals = {}
    for place in all_places:
        linked_animals.update({place["id"]: [animal['animalID'] for animal in (animal_place_services.get_animals_linked_to_place(place["id"]))]})

    context = {
        "segment": "places",
        "places": all_places,
        "linked_animals": linked_animals,
        "form": form,
    }

    return render(request, "home/show_places.html", context)


@login_required(login_url="/login/")
def delete_place(request, place_id):
    place_services.delete_place(place_id)
    messages.success(request, "Place deleted successfully")
    return redirect("places")


@login_required(login_url="/login/")
def add_animal_to_place(request, animal_id, place_id):
    animal_place_services.add_animal_to_place(animal_id, place_id)
    messages.success(request, "Animal assigned successfully")
    return redirect("places")


@login_required(login_url="/login/")
def edit_place(request, place_id):
    place = place_services.get_place(place_id)

    if request.method == "POST":
        form = place_forms.PlaceForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data

            name = data["name"]
            description = data["description"]
            isOpen = data["isOpen"]
            image = data["image"]

            place_services.edit_place(place_id, name, description, isOpen, image)

            messages.success(request, f""""{name}" edited successfully""")

            return redirect("places")
        else:
            form = place_forms.PlaceForm()
    else:
        form = place_forms.PlaceForm()
        form.fields["name"].initial = place["name"]
        form.fields["description"].initial = place["description"]
        form.fields["isOpen"].initial = place["isOpen"]
        form.fields["image"].initial = place["image"]

    animals = []
    linked_animals = animal_place_services.get_animals_linked_to_place(place_id)
    linked_animals = get_ids_from_filter(linked_animals, "animalID")
    all_animals = animal_services.get_animals_list()
    for item in all_animals:
        if not item["id"] in linked_animals:
            animals.append(item)

    context = {
        "segment": "places",
        "place": place,
        "place_id": place_id,
        "animals": animals,
        "linked_animals": linked_animals,
        "form": form,
    }

    return render(request, "home/edit_place.html", context)


@login_required(login_url="/login/")
def remove_animal_from_place(request, animal_id, place_id):
    animal_place_services.remove_animal_from_place(animal_id, place_id)
    messages.success(request, "Animal detached successfully")
    return redirect("places")
