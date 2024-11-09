from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from ..services import user_services


@login_required(login_url="/login/")
def all_users(request, page_token=None):
    users = user_services.get_users_list(page_token)
    # print(users)

    context = {
        'segment': 'users',
        'users': users,
    }

    html_template = loader.get_template('home/show_users.html')
    return HttpResponse(html_template.render(context, request))
