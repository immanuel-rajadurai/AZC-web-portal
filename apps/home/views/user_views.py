from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from ..services import user_services


@login_required(login_url="/login/")
def all_users(request):
    token = request.POST.get('token')

    users = user_services.get_users_list(token)
    # print("users: ", users)

    if token is None:
        isFirstPage = True
    else:
        isFirstPage = False

    context = {
        'segment': 'users',
        'users': users,
        'isFirstPage': isFirstPage,
    }

    html_template = loader.get_template('home/show_users.html')
    return HttpResponse(html_template.render(context, request))
