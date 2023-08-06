# -*- coding: utf-8 -*-
from time import sleep
from .api import ListoAPI, TooManyRequests


class Banks(ListoAPI):
    def __init__(self, token, base_url):
        super(Banks, self).__init__(token, base_url)

    def get_bank_accounts(self):
        return self.make_request(method="GET", path="/banks/bank_transaction/facets") \
               .json()['facets']['bank_account']
