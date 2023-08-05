# -*- coding: utf-8 -*-
from .api import ListoAPI


class Setup(ListoAPI):
    def __init__(self, token, base_url):
        super(Setup, self).__init__(token, base_url)

    def validate_ciec(self, rfc, ciec):
        """Validate ciec password for a RFC

        Args:
            - rfc (str): RFC of the business
            - ciec (str): CIEC password
        """
        return self.make_request(method="POST", path="/signup/verify_ciec", json=dict(rfc=rfc, ciec=ciec)).json()

    def add_main_user(self, rfc, ciec, sat_sync_since="2016-01-01", sat_sync_webhook_url=""):
        """Register a new business

        Args:
            - rfc (str): RFC of the business
            - ciec (str): CIEC password
            - sat_sync_since (str): ISO format YYYY-mm-dd date from which invoices will download
            - sat_sync_webhook_url (str): Webhook URL to receive notifications after successful downloads
        """
        return self.make_request(method="POST", path="/signup/external", json=dict(rfc=rfc, ciec=ciec,
                                 sat_sync_since=sat_sync_since, sat_sync_webhook_url=sat_sync_webhook_url)).json()

    def modify_ciec(self, rfc_id, ciec):
        """Change CIEC password for an rfc_id

        Args:
            - rfc_id (str|int)
            - ciec (str): new ciec password
        """
        return self.make_request(method="POST", path="/customers/rfcs/%s/enable_sat_sync" % rfc_id,
                                 json={"ciec": ciec}).json()

    def view_rfcs(self):
        """List all rfcs the token has access to"""
        return self.make_request(method="GET", path="/customers/rfcs/").json()

    def lookup_rfc(self, rfc):
        """List all rfcs the token has access to"""
        return self.make_request(method="GET", path="/signup/lookup_rfc/%s" % rfc).json()

    def add_rfc(self, **kwargs):
        """Add rfc to a user

        Kwargs:
        - colonia
        - ext_num
        - int_num
        - locality
        - mailbox_suffix: <main_username>+<mailbox_suffix>@buzon.listo.mx
        - municipio
        - postal_code
        - rfc
        - rfc_name
        - state
        - street
        - tax_regime: Possible values are {pf_asalariado, pf_profesional, pf_rif, pm, pm_nonprofit}
        """
        return self.make_request(method="POST", path="/customers/rfcs/", data=kwargs).json()
