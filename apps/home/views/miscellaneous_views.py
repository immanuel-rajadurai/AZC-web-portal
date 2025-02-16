from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from ..services import occurence_counter_services
from extras import setListToLength


@login_required(login_url="/login/")
def statistics(request):
    numberOfVisitors = occurence_counter_services.get_occurence_history(
        "numberOfVisitors"
    )
    numberOfVisitors = setListToLength(numberOfVisitors, 12)
    print("numberOfVisitors", numberOfVisitors)

    animalChallengeCompletions = occurence_counter_services.get_occurence_history(
        "animalChallengeCompletions"
    )
    animalChallengeCompletions = setListToLength(
        animalChallengeCompletions, 12)
    print("animalChallengeCompletions", animalChallengeCompletions)

    context = {
        "segment": "index",
        "numberOfVisitors": numberOfVisitors,
        "animalChallengeCompletions": animalChallengeCompletions,
    }

    html_template = loader.get_template("home/statistics.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:
        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))

        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))
