from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..services import user_services


class PageList:
    def reset(self):
        self.lst = [None]
        self.currentPageNum = 0

    def __init__(self):
        self.reset()

    def __str__(self):
        return f"{self.lst}\n{self.currentPageNum}"

    def add_page(self, token):
        self.lst.append(token)

    def is_first_page(self):
        if self.currentPageNum == 0:
            return True
        return False

    def next_page(self):
        self.currentPageNum += 1
        return self.lst[self.currentPageNum]

    def previous_page(self):
        self.currentPageNum -= 1
        return self.lst[self.currentPageNum]


PAGE_LIST = PageList()


@login_required(login_url="/login/")
def all_users(request, actionCode=None):
    global PAGE_LIST

    if actionCode == 0:
        token = PAGE_LIST.previous_page()
    elif actionCode == 1:
        token = PAGE_LIST.next_page()
    else:
        token = None
        PAGE_LIST.reset()

    users = user_services.get_users_list(token)
    PAGE_LIST.add_page(users['nextToken'])

    # print("PAGE-LIST", PAGE_LIST)

    context = {
        'segment': 'users',
        'users': users,
        'isFirstPage': PAGE_LIST.is_first_page(),
    }

    return render(request, 'home/show_users.html', context)
