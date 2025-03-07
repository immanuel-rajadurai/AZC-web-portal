from django.http import HttpResponse
import pandas as pd
from ...services import user_services


def download_opted_in_users():
    users = user_services.get_opted_in_users()
    filename = "opted_in_users.csv"

    df = pd.DataFrame(users, columns=["email", "firstName", "lastName", "optedIn"])
    df.to_csv(filename, index=False)

    fl = open(filename, "r")

    response = HttpResponse(fl, content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


class PageList:
    def reset(self):
        self.__lst = [None]
        self.__currentPageNum = 0

    def __init__(self):
        self.__lst = None
        self.__currentPageNum = None
        self.reset()

    def __str__(self):
        return f"{self.__lst}\n{self.__currentPageNum}"

    def add_page(self, token):
        self.__lst.append(token)

    def is_first_page(self):
        if self.__currentPageNum == 0:
            return True
        return False

    def next_page(self):
        self.__currentPageNum += 1
        return self.__lst[self.__currentPageNum]

    def previous_page(self):
        self.__currentPageNum -= 1
        return self.__lst[self.__currentPageNum]
