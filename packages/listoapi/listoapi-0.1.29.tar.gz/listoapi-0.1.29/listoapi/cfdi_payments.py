# -*- coding: utf-8 -*-
from .api import ListoAPI


class CfdiPayments(ListoAPI):
    def __init__(self, token, base_url):
        super(CfdiPayments, self).__init__(token, base_url)

    def cfdi_payments(self, **kwargs):
        """CFDI Payments
        Note: Size larger than 200 causes 500 Error

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/cfdi_payments/payments/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size

    def cfdi_receipts(self, **kwargs):
        """CFDI Receipts
        Note: Size larger than 200 causes 500 Error

        """
        kwargs.setdefault("offset", 0)
        size = kwargs.setdefault("size", 100)
        while True:
            r = self.make_request(
                method="GET", path="/cfdi_payments/receipts/",
                params=kwargs).json()["hits"]
            if not r:
                break
            for i in r:
                yield i
            kwargs["offset"] += size
