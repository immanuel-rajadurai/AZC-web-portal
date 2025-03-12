from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..services import user_services
from .extras.user_views_extras import download_opted_in_users, PageList

PAGE_LIST = PageList()

@login_required(login_url="/login/")
def all_users(request, actionCode=None):
    global PAGE_LIST

    if actionCode == 0:
        token = PAGE_LIST.backward()
    elif actionCode == 1:
        token = PAGE_LIST.forward()
    elif actionCode == 2:
        return download_opted_in_users()
    else:
        token = None
        PAGE_LIST.reset()

    users = user_services.get_users_list(token)
    PAGE_LIST.add_page(users["nextToken"])

    context = {
        "segment": "users",
        "users": users,
        "isFirstPage": PAGE_LIST.is_first_page(),
    }

    return render(request, "home/show_users.html", context)
