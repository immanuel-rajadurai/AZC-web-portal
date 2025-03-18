from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from ..services import animal_services
from ..forms import animal_forms


@login_required(login_url="/login/")
def all_animals(request):
    if request.method == "POST":
        form = animal_forms.AnimalForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            scientificName = form.cleaned_data["scientificName"]
            habitat = form.cleaned_data["habitat"]
            diet = form.cleaned_data["diet"]
            behaviour = form.cleaned_data["behaviour"]
            weightMale = form.cleaned_data["weightMale"]
            weightFemale = form.cleaned_data["weightFemale"]
            image = form.cleaned_data["image"]
            conservationStatus = form.cleaned_data["conservationStatus"]
            funFacts = form.cleaned_data["funFacts"]
            animal_services.add_animal(name, scientificName, habitat, diet, behaviour,
                                       weightMale, weightFemale, image, conservationStatus, funFacts)

            messages.success(request, "Animal created successfully")
        else:
            messages.error(request, "Animal not created, check formatting")

    form = animal_forms.AnimalForm()

    context = {
        "segment": "animals",
        "animals": animal_services.get_animals_list(),
        "form": form,
    }

    return render(request, "home/show_animals.html", context)


def remove_animal(request, animal_id):
    if request.user.is_authenticated:
        animal_services.remove_animal(animal_id)
        messages.success(request, "Animal removed successfully")

    return redirect("animals")


def edit_animal(request, animal_id):
    animal = animal_services.get_animal(animal_id)
    
    if request.user.is_authenticated and animal is not None:
        if request.method == "POST":
            form = animal_forms.AnimalForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data["name"]
                scientificName = form.cleaned_data["scientificName"]
                habitat = form.cleaned_data["habitat"]
                diet = form.cleaned_data["diet"]
                behaviour = form.cleaned_data["behaviour"]
                weightMale = form.cleaned_data["weightMale"]
                weightFemale = form.cleaned_data["weightFemale"]
                image = form.cleaned_data["image"]
                conservationStatus = form.cleaned_data["conservationStatus"]
                funFacts = form.cleaned_data["funFacts"]
                animal_services.edit_animal(animal_id, name, scientificName, habitat, diet,
                                            behaviour, weightMale, weightFemale, image, conservationStatus, funFacts)

                messages.success(request, f""""{name}" edited successfully""")
                return redirect("animals")
        else:
            form = animal_forms.AnimalForm()
            form.fields["name"].initial = animal["name"]
            form.fields["scientificName"].initial = animal["scientificName"]
            form.fields["habitat"].initial = animal["habitat"]
            form.fields["diet"].initial = animal["diet"]
            form.fields["behaviour"].initial = animal["behaviour"]
            form.fields["weightMale"].initial = animal["weightMale"]
            form.fields["weightFemale"].initial = animal["weightFemale"]
            form.fields["image"].initial = animal["image"]
            form.fields["conservationStatus"].initial = animal["conservationStatus"]
            form.fields["funFacts"].initial = animal["funFacts"]

        context = {
            "segment": "animals",
            "animal": animal,
            "form": form,
        }

        return render(request, "home/edit_animal.html", context)
    else:
        return redirect("animals")
