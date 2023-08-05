# -*- coding: utf-8 -*-
from .api import ListoAPI


class Expenses(ListoAPI):
    def __init__(self, token, base_url):
        super(Expenses, self).__init__(token, base_url)

    def get_accounts(self, **kwargs):
        """Expenses Accounts

        """
        r = self.make_request(
            method="GET", path="/expenses/expense_accounts/",
            params=kwargs).json()["hits"]
        for i in r:
            yield i

    def get_reimbursements(self, **kwargs):
        """Expenses Reimbursements

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/expenses/reimbursements/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def get_expenses(self, **kwargs):
        """Expenses Expenses

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/expenses/expenses/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size
