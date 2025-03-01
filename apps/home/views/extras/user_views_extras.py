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
        self.lst = [None]
        self.currentPageNum = 0

    def __init__(self):
        self.lst = None
        self.currentPageNum = None
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