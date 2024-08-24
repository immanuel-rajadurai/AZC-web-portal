# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.services.events import create_event, get_events_list
from .forms import EventForm
from django.shortcuts import render, redirect
from django.contrib import messages


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    print("now entering a HTML page")
    print(request.path)
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def events(request):

    if request.method == 'POST':
        print("executing post request")
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            print("form data: ", data)

            name = data['name']
            description = data['description']
            image = data['image']

            create_event(name, description, image)

            messages.success(request, 'Event created successfully')

            # return redirect('success')
    else:
        form = EventForm()


    events_data_test = [
        {'name': 'Event 1', 'description': 'this is the description', 'image': 'Location 1'},
        {'name': 'Event 1', 'description': 'this is the description', 'image': 'Location 1'},
        {'name': 'Event 1', 'description': 'this is the description', 'image': 'Location 1'},
    ]

    events_data = get_events_list()

    context = {
        'segment': 'events',
        'events': events_data,
        'form': form,
    }


    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))