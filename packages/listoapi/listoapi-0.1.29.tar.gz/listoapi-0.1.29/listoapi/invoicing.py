# -*- coding: utf-8 -*-
import base64
import os
import ssl
import subprocess
import sys

from OpenSSL import crypto
from .api import ListoAPI, ResourceNotFound


class InvalidRFCId (ResourceNotFound):
    pass


class Invoicing(ListoAPI):
    """Invoicing class

    Args:
        - token (str): Listo API token
        - cer_path (str): Path to the .cer file
        - key_path (str): Path to the .key file
        - key_passphrase (str): .key file password
    """
    def __init__(self, token, cer_path, key_path, key_passphrase, base_url):
        super(Invoicing, self).__init__(token, base_url)
        self.CER_PATH = cer_path
        self.KEY_PATH = key_path
        self.PRIVATE_KEY_PASSPHRASE = key_passphrase

        self._read_cer()
        self._read_key()

    # Private for create XML
    def _generate_xml(self, generation_data):
        return self.make_request(method="POST", json=generation_data,
                                 path="/invoicing/generate_xml")

    # Private send data and XML to certify in Listo.mx
    def _certify_xml(self, certification_data):
        return self.make_request(method="POST", json=certification_data,
                                 path="/invoicing/certify_xml")

    def _cancel(self, gii, certification_data):
        return self.make_request(method="POST", json=certification_data,
                                 path="/invoicing/invoices/%s/cancel" % gii)

    # Private for read certificate
    def _read_cer(self):
        with open(self.CER_PATH, 'rb') as f:
            self.cert_der = f.read()
            self.cert = crypto.load_certificate(
                crypto.FILETYPE_PEM, ssl.DER_cert_to_PEM_cert(self.cert_der))
        self.certificate_num = ('%0x' % self.cert.get_serial_number())[1::2]

    # Private for read key
    def _read_key(self):
        with open(self.KEY_PATH, 'rb') as f:
            self.private_key_der = f.read()

        if 'win' in sys.platform:
            args = ['%s/openssl' % os.path.dirname(os.path.realpath(__file__)), 'pkcs8', '-inform', 'DER', '-passin', 'pass:' + self.PRIVATE_KEY_PASSPHRASE]
        else:
            args = ['openssl', 'pkcs8', '-inform', 'DER', '-passin', 'pass:' + self.PRIVATE_KEY_PASSPHRASE]
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        private_pem = proc.communicate(input=self.private_key_der)[0].strip()
        self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_pem)

    def cancel(self, gid):
        """Cancel Invoice
        Args:
            gid: invoice.generated_invoice_id, do not mistake with invoice.id
        """
        cd = {
            "certificate_der": base64.b64encode(self.cert_der).decode("utf-8"),
            "passcode": self.PRIVATE_KEY_PASSPHRASE,
            "private_key_der": base64.b64encode(self.private_key_der).decode("utf-8"),
        }
        return self._cancel(gid, cd).json()

    def email_invoice(self, gid, **kwargs):
        """Email invoice
        Args:
            gid: invoice.generated_invoice_id, do not mistake with invoice.id. In that case use Invoices.send_by_email
            from: email who will send it
            to: receiver email
            subject: email subject
            text: Message body in text
            html: Message body in html format
        """
        return self.make_request(method="POST", json=kwargs,
                                 path="/invoicing/invoices/%s/email" % gid)

    def customer_rfcs(self):
        """Data from default_rfc_id, employees, receivers, issuers and branches """
        return self.make_request(method="GET", path="/invoicing/customer/rfcs/").json()

    def generate(self, generation_data, certify=False):
        """Generate XML, Sign it and get SAT stamp

        Args:
            - generation_data ([]): array of invoice data to generate
            - testing (bool): If True do not send to SAT for stamping. Default True
        """
        # Validate data
        for gd in generation_data:
            self.validate_rfc(gd["issuer"]["rfc"])
            self.validate_rfc(gd["receiver"]["rfc"])

        # Generate XML
        try:
            r = self._generate_xml(generation_data).json()
        except ResourceNotFound:
            raise InvalidRFCId("issuer.id %s does not match token's user" % gd["issuer"]["id"])

        for c, gd in zip(r, generation_data):
            # c contains xml and original_chain
            xml = c['xml']

            # Replace certificate number in original chain
            original_chain = c['original_chain'].replace('|' + '0' * 20 + '|', '|%s|' % self.certificate_num)

            # Verification and signature
            signature = crypto.sign(self.key, original_chain, 'sha256')
            crypto.verify(self.cert, signature, original_chain, 'sha256')

            # Object to stamp
            certification_data = {
                'xml': xml,
                'certificate_num': self.certificate_num,
                'certificate': base64.b64encode(self.cert_der).decode("utf-8"),
                'signature': base64.b64encode(signature).decode("utf-8"),
                'data': gd
            }

            if certify:
                r = self._certify_xml(certification_data).json()
                yield r, certification_data, original_chain
            else:
                yield {}, certification_data, original_chain
