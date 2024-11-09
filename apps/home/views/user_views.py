from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from ..services import user_services


@login_required(login_url="/login/")
def all_users(request):
    if not 'users_list_nextToken' not in request.session:
        users_list_nextToken = None
    else:
        users_list_nextToken = request.session['users_list_nextToken']

    users = user_services.get_users_list(users_list_nextToken)
    print(users)

    request.session['users_list_nextToken'] = users["nextToken"]

    context = {
        'segment': 'users',
        'users': users,
    }

    html_template = loader.get_template('home/show_users.html')
    return HttpResponse(html_template.render(context, request))
