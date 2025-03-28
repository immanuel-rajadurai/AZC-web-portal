from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from ..services import (
    event_services,
    place_event_services,
    place_services,
    event_tag_services,
    tag_services,
)
from ..forms import event_forms
from .miscellaneous_views import get_ids_from_filter
from .views_extras import split_tags


@login_required(login_url="/login/")
def all_events(request):
    if request.method == "POST":
        form = event_forms.EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            name = data["name"]
            description = data["description"]
            image = data["image"]
            event_id = event_services.create_event(name, description, image)

            tags = data["tags"]
            tags = split_tags(tags)

            for tagName in tags:
                event_tag_services.create_tag(event_id, tagName)

            messages.success(request, "Event created successfully")

    form = event_forms.EventForm()

    events = event_services.get_events_list()

    linked_places = {}
    linked_tags = {}
    for event in events:
        tmp = place_event_services.get_places_linked_to_event(event["id"])
        tmp = get_ids_from_filter(tmp, "placeID")
        linked_places.update({event["id"]: tmp})

        tags = event_tag_services.get_tags(event["id"])
        tmp = []
        for tag in tags:
            if tag["tagName"] != "":
                tmp.append(tag["tagName"])

        linked_tags.update({event["id"]: tmp})

    context = {
        "segment": "events",
        "events": events,
        "all_tags": tag_services.get_tags_list(),
        "linked_places": linked_places,
        "linked_tags": linked_tags,
        "form": form,
    }

    return render(request, "home/show_events.html", context)


@login_required(login_url="/login/")
def delete_event(request, event_id):
    event_services.delete_event(event_id)
    messages.success(request, "Event deleted successfully")
    return redirect("events")


@login_required(login_url="/login/")
def add_place_to_event(request, place_id, event_id):
    place_event_services.add_place_to_event(event_id, place_id)
    messages.success(request, "Place assigned successfully")
    return redirect("events")


@login_required(login_url="/login/")
def edit_event(request, event_id):
    event = event_services.get_event(event_id)

    if request.method == "POST":
        form = event_forms.EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            name = data["name"]
            description = data["description"]
            image = data["image"]

            event_services.edit_event(event_id, name, description, image)

            existing_tags = event_tag_services.get_tags(event_id)

            input_tags = data["tags"]
            input_tags = split_tags(input_tags)

            for tag in input_tags:
                if not tag in existing_tags:
                    event_tag_services.create_tag(event_id, tag)

            for tag in existing_tags:
                if not tag["tagName"] in input_tags:
                    event_tag_services.delete_tag(event_id, tag["tagName"])

            messages.success(request, f""""{name}" edited successfully""")

            return redirect("events")
    else:
        form = event_forms.EventForm()
        form.fields["name"].initial = event["name"]
        form.fields["description"].initial = event["description"]
        form.fields["image"].initial = event["image"]

        linked_tags = event_tag_services.get_tags(event_id)
        tags = []
        for tag in linked_tags:
            if tag["tagName"] != "":
                tags.append(tag["tagName"])

        form.fields["tags"].initial = ", ".join(tags)

    linked_places = place_event_services.get_places_linked_to_event(event_id)
    linked_places = get_ids_from_filter(linked_places, "placeID")

    all_places = place_services.get_places_list()
    places = []
    for item in all_places:
        if not item["id"] in linked_places:
            places.append(item)

    context = {
        "segment": "events",
        "event": event,
        "all_tags": tag_services.get_tags_list(),
        "event_id": event_id,
        "places": places,
        "linked_places": linked_places,
        "linked_tags": linked_tags,
        "form": form,
    }

    return render(request, "home/edit_event.html", context)


@login_required(login_url="/login/")
def remove_place_from_event(request, place_id, event_id):
    place_event_services.remove_place_from_event(place_id, event_id)
    messages.success(request, "Place detached successfully")
    return redirect("events")
