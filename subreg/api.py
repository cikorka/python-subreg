# -*- coding: utf-8 -*-

# Copyright (c) 2013 Petr Jerabek
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

import re
from SOAPpy import SOAPProxy, typedArrayType

from .exceptions import ApiError


class Api(object):
    """Python wrapper around the subreg.cz SOAP API"""

    endpoint = 'https://soap.subreg.cz/cmd.php'

    response = None
    """Last parsed response from API"""

    raw_response = None
    """Last raw response from API"""

    def __init__(self, username=None, password=None):
        """"""
        self.token = None
        self.client = SOAPProxy(self.endpoint)
        if username and password:
            self.login(username, password)

    def login(self, username=None, password=None):
        """
        User login to API

        :param username: Username for login
        :param password: Password

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Login
        """
        kwargs = {'login': username, 'password': password}
        response = self._request('Login', kwargs)
        self.token = response['ssid']

    def check_domain(self, domain):
        """
        Check if domain is available or not

        :param domain: Domain for check availability

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Check_Domain
        """
        kwargs = {'domain': domain}
        response = self._request('Check_Domain', kwargs)
        if response['avail'] == 1:
            return True
        return False

    def info_domain(self, domain):
        """
        Get informations about a single domain from your account

        :param domain: Domain name for requested informations

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Info_Domain
        """
        kwargs = {'domain': domain}
        response = self._request('Info_Domain', kwargs)
        return response

    def info_domain_cz(self, domain):
        """
        Get informations about a single .CZ domain

        :param domain: Domain name for requested informations

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Info_Domain_CZ
        """
        kwargs = {'domain': domain}
        response = self._request('Info_Domain_CZ', kwargs)
        return response

    def domains_list(self):
        """
        Get all domains from your account

        :return dict
            :key `domains`: dict of domains
                :key `name`: Domain name
                :key `expire`: Domain expiration date
            :key `count`: Domains count

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Domains_List
        """
        return self._request('Domains_List')

    def set_autorenew(self, domain, autorenew):
        """
        Set autorenew policy for your domain.
        By default, domain is deleted when it expire.
        You can set autorenew flag to AUTORENEW, then it will use your credit
        to renew automatically. RENEWONCE will cause renew only for next year.

        :param domain: Registered domain
        :param autorenew: Autorenew setting, allowed values:
            EXPIRE, AUTORENEW, RENEWONCE

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Set_Autorenew
        """
        if autorenew in ['EXPIRE', 'AUTORENEW', 'RENEWONCE']:
            kwargs = {'domain': domain, 'autorenew': autorenew}
            try:
                self._request('Set_Autorenew', kwargs)
                return True
            except ApiError:
                return False
        return False

    def create_contact(self, **kwargs):
        """
        Create contact in Subreg DB

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Create_Contact
        """
        raise NotImplementedError

    def update_contact(self, **kwargs):
        """
        Update contact

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Update_Contact
        """
        raise NotImplementedError

    def info_contact(self, contact_id):
        """
        Get informations about a single contact from your account

        :param contact_id: ID of your querying contact

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Info_Contact
        """
        raise NotImplementedError

    def contacts_list(self):
        """
        Get all contacts from your account

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Contacts_List
        """
        return self._request('Contacts_List')

    def check_object(self, _id, _object):
        """
        Check if object is available or not (only CZ,EE)

        :param _id: ID for check availability
        :param _object: contact, nsset, keyset (only CZ, EE)

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Check_Object
        """
        raise NotImplementedError

    def info_object(self, _id, _object):
        """
        Info about NIC object (only CZ,EE)

        :param _id: ID for info
        :param _object: contact, nsset, keyset (only CZ, EE)

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Info_Object
        """
        raise NotImplementedError

    def make_order(self, **kwargs):
        """
        Create a new order (CreateDomain, ModifyDomain, RenewDomain, ... )

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Make_Order
        """
        raise NotImplementedError

    def info_order(self, order_id):
        """
        Info about existing order

        :param order_id: Order ID

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Info_Order
        """
        raise NotImplementedError

    def get_credit(self):
        """
        Get status of your credit

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Get_Credit
        """
        return self._request('Get_Credit')

    def get_accountings(self, from_date, to_date):
        """
        Get financial statements from account

        :param from_date: Date (YYYY-mm-dd)
        :param to_date: Date (YYYY-mm-dd)

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Get_Accountings
        """
        raise NotImplementedError

    def client_payment(self, username, amount, currency):
        """
        Add credit to your sub-user. This command WILL generate invoice,
        if you want just correct current amount of credit for any reason,
        please use command Credit_Correction.

        :param username: Login username of the use you want to add credit
        :param amount: Amount of money to add
        :param currency: Currency of added credit

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Client_Payment
        """
        raise NotImplementedError

    def credit_correction(self, username, amount, reason):
        """
        Correct credit amount of your sub-users. The amount you specify in this
        command will be added to current amount. Use negative values for
        subtracting credit. Please note that currency will depend on
        current user setting.

        :param username: Login username of the user you want to add credit
        :param amount: Amount of money to add/subtract
        :param reason: Human readable reason for this operation

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Credit_Correction
        """
        raise NotImplementedError

    def pricelist(self):
        """
        Get pricelist from account

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Pricelist
        """
        return self._request('Pricelist')

    def prices(self, tld):
        """
        Get Prices for TLD from account

        :type tld: Requested TLD

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Prices
        """
        raise NotImplementedError

    def get_pricelist(self, pricelist):
        """
        Return all price information in specified pricelist.

        :param pricelist: Identificator of the pricelist you want to download.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Get_Pricelist
        """
        raise NotImplementedError

    def set_prices(self, pricelist, tld, currency, prices=None):
        """
        Change prices in specified pricelist.

        :param pricelist: Identificator of the pricelist you want to download.
        :param tld: TLD for which you want to change prices.
        :param currency: Currency code the prices use.
        :param prices: List of operations with price

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Set_Prices
        """
        raise NotImplementedError

    def download_document(self, document_id):
        """
        Get document information and base64 encoded document that you have
        uploaded or generated on your account.

        :param document_id: Document ID, you can get it in response of
                            `Upload_Document` or by `List_Documents`.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Download_Document
        """
        raise NotImplementedError

    def upload_document(self, name, document, _type=None, filetype=None):
        """
        Upload document to your account, for use as identification document,
        registration request etc.

        :param name: Filename of the document, including extension
        :param document: base64 encoded document
        :param _type: Type of the document
                     (https://soap.subreg.cz/manual/?cmd=Document_Types)
        :param filetype: MIME type of the file

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Upload_Document
        """
        raise NotImplementedError

    def list_documents(self):
        """
        List documents uploaded or generated on your account.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=List_Documents
        """
        return self._request('List_Documents')

    def users_list(self):
        """
        Retrieve list of all your sub-users

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Users_List
        """
        return self._request('Users_List')

    def get_dns_zone(self, domain):
        """
        List of DNS records for specified domain.

        :param domain: Registered domain

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Get_DNS_Zone
        """
        kwargs = {'domain': domain}
        response = self._request('Get_DNS_Zone', kwargs)
        try:
            return response['records']
        except KeyError:
            return []

    def add_dns_zone(self, domain, template=None):
        """
        Add domain to DNS using previously created template.

        :param domain: Registered domain
        :param template: DNS template ID or template name

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Add_DNS_Zone
        """
        kwargs = {'domain': domain}
        if not template:
            kwargs['template'] = template
        try:
            self._request('Add_DNS_Zone', kwargs)
            return True
        except ApiError:
            return False

    def delete_dns_zone(self, domain):
        """
        Remove ALL DNS records for specified domain.

        :param domain: Registered domain

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Delete_DNS_Zone
        """
        kwargs = {'domain': domain}
        response = self._request('Delete_DNS_Zone', kwargs)
        return response

    def set_dns_zone(self, domain, records):
        """
        Specify complete set of records for certain zone.
        Specified records will replace ALL present records.

        :param domain: Registered domain
        :param records: List of dicts of records

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Set_DNS_Zone
        """
        raise NotImplementedError

    def add_dns_record(self, domain, record):
        """
        Add DNS record to zone.

        :param domain: Registered domain
        :param record: dict with params

            :key name: Hostname (part of hostname, without registered domain)
            :key type: Type of DNS record
            :key content: Value of this record (IP address, hostname, text
                value,..)
            :key prio: Priority of this record (MX records only)
            :key ttl: TTL value

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Add_DNS_Record
        """
        if not isinstance(record, dict):
            raise TypeError
            # remove leading .
        record['content'] = re.sub('\.$', '', record['content'])
        kwargs = {'domain': domain, 'record': record}
        try:
            response = self._request('Add_DNS_Record', kwargs)
            return response['record_id']
        except (KeyError, ApiError):
            return False

    def modify_dns_record(self, domain, record):
        """
        Midify DNS record at zone.

        :param domain: Registered domain
        :param record: dict with ID of existing record

            :key id: ID of existing record
            :key name: Hostname (part of hostname, without registered domain)
            :key type: Type of DNS record
            :key content: Value of this record (IP address, hostname, text
                value,..)
            :key prio: Priority of this record (MX records only)
            :key ttl: TTL value

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Modify_DNS_Record
        """
        if not isinstance(record, dict):
            raise TypeError
        error_message = 'You must specify `record.id` when edit record.'
        try:
            if not record['id']:
                raise Exception(error_message)
        except KeyError:
            raise Exception(error_message)
        kwargs = {'domain': domain, 'record': record}
        try:
            self._request('Modify_DNS_Record', kwargs)
            return True
        except (KeyError, ApiError):
            return False

    def delete_dns_record(self, domain, record_id):
        """
        Remove DNS record from zone.

        :param domain: Registered domain
        :param record_id: ID of existing record

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Delete_DNS_Record
        """
        if not record_id:
            raise TypeError
        kwargs = {'domain': domain, 'record': {'id': record_id}}
        try:
            self._request('Delete_DNS_Record', kwargs)
            return True
        except ApiError:
            return False

    def poll_get(self):
        """
        Get current poll message

        .. seealso:: https://soap.subreg.cz/manual/?cmd=POLL_Get
        """
        return self._request('POLL_Get')

    def poll_ack(self, poll_id):
        """
        Ack current poll message

        :param poll_id: POLL ID

        .. seealso:: https://soap.subreg.cz/manual/?cmd=POLL_Ack
        """
        raise NotImplementedError

    def oib_search(self, oib):
        """
        List domains registered for certain OIB, and get the number of domains
        possible to register for this OIB.

        :param oib: Croatian OIB number

        .. seealso:: https://soap.subreg.cz/manual/?cmd=OIB_Search
        """
        raise NotImplementedError

    def create_domain(self):
        """Order: `Create_Domain`
        Create a new domain.
        For DNSSEC extension please see full
        specification `here <https://soap.subreg.cz/manual/?cmd=DNSSEC>`_

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Create_Domain
        """
        raise NotImplementedError

    def transfer_domain(self):
        """
        Transfer domain between two registrars or two account

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Transfer_Domain
        """
        raise NotImplementedError

    def account_transfer_domain(self):
        """
        Transfer domain between two Subreg.CZ accounts.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=AccountTransfer_Domain
        """
        raise NotImplementedError

    def transfer_approve_domain(self):
        """
        Transfer Approve domain between two registrars

        .. seealso:: https://soap.subreg.cz/manual/?cmd=TransferApprove_Domain
        """
        raise NotImplementedError

    def transfer_deny_domain(self):
        """
        Transfer Deny domain between two registrars

        .. seealso:: https://soap.subreg.cz/manual/?cmd=TransferDeny_Domain
        """
        raise NotImplementedError

    def transfer_cancel_domain(self):
        """
        Transfer Cancel domain between two registrars

        .. seealso:: https://soap.subreg.cz/manual/?cmd=TransferCancel_Domain
        """
        raise NotImplementedError

    def sk_change_owner_domain(self):
        """
        Initiate owner change for .SK domain. During processing of this order,
        filled form will be generated onto your account.
        You can then download it using our web interface or using
        `Download_Document <https://soap.subreg.cz/manual/?cmd=Download_Document>`_.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=SKChangeOwner_Domain
        """
        raise NotImplementedError

    def modify_domain(self):
        """
        Modify existing domain to new values.
        For DNSSEC extension please see full
        specification `here <https://soap.subreg.cz/manual/?cmd=DNSSEC>`_.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Modify_Domain
        """
        raise NotImplementedError

    def modify_ns_domain(self):
        """
        Modify existing domain to new values.
        For DNSSEC extension please see full
        specification `here <https://soap.subreg.cz/manual/?cmd=DNSSEC>`_.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=ModifyNS_Domain
        """
        raise NotImplementedError

    def delete_domain(self):
        """
        Delete a existing domain from your account

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Delete_Domain
        """
        raise NotImplementedError

    def restore_domain(self):
        """
        Restore a deleted domain from your account

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Restore_Domain
        """
        raise NotImplementedError

    def renew_domain(self):
        """
        Renew a existing domain from your account

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Renew_Domain
        """
        raise NotImplementedError

    def backorder_domain(self):
        """
        Create a backorder order. We will register domain after deletion
        from registry

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Backorder_Domain
        """
        raise NotImplementedError

    def preregister_domain(self):
        """
        This order type is for new TLDs or liberation rules of existing TLDs
        domain pre-registration

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Preregister_Domain
        """
        raise NotImplementedError

    def create_object(self):
        """
        Creates new nsset or keyset.
        Only for registries with such capability (for example CZ-NIC or Eurid)

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Create_Object
        """
        raise NotImplementedError

    def transfer_object(self):
        """
        Transfer object between two registrars (CZ-NIC)

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Transfer_Object
        """
        raise NotImplementedError

    def update_object(self):
        """
        .. seealso:: https://soap.subreg.cz/manual/?cmd=Update_Object
        """
        raise NotImplementedError

    def transfer_ru_request(self):
        """
        Transfer (change partner) of all domains on specified NIC-D account to
        Subreg.CZ.
        If you want to transfer just one .ru domain, you need to create new
        NIC-D account for that domain.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=TransferRU_Request
        """
        raise NotImplementedError

    def create_host(self):
        """
        Create new delegated host object.
        It is possible to specify multiple IPv4 and IPv6 addresses of the host.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Create_Host
        """
        raise NotImplementedError

    def update_host(self):
        """
        Change IP addresses of delegated host object.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Update_Host
        """
        raise NotImplementedError

    def delete_host(self):
        """
        Delete delegated host object.
        It is only possible to delete host when it is no longer used.

        .. seealso:: https://soap.subreg.cz/manual/?cmd=Delete_Host
        """
        raise NotImplementedError

    def set_google_mx_records(self, domain):
        """
        Set Google MX rerods.
        Specified records will replace ALL present MX records.
        """
        records = self.get_dns_zone(domain)
        for record in records:
            # delete all mx records
            if record['type'] == 'MX':
                self.delete_dns_record(domain, record['id'])

        records = [
            dict(content='ASPMX.L.GOOGLE.COM.', prio=1),
            dict(content='ALT1.ASPMX.L.GOOGLE.COM.', prio=5),
            dict(content='ALT2.ASPMX.L.GOOGLE.COM.', prio=5),
            dict(content='ASPMX2.GOOGLEMAIL.COM.', prio=10),
            dict(content='ASPMX3.GOOGLEMAIL.COM.', prio=10),
        ]
        for record in records:
            record['ttl'] = 3600
            record['type'] = 'MX'
            self.add_dns_record(domain, record)

    def _request(self, command, kwargs=None):
        """Make request parse response"""
        if kwargs is None:
            kwargs = dict()
        if self.token:
            kwargs['ssid'] = self.token
        method = getattr(self.client, command)
        raw_response = method(**dict(data=kwargs))
        response = self._parse_response(raw_response)
        self.response = response
        self.raw_response = raw_response
        if response:
            if response['status'] == 'error':
                raise ApiError(
                    'Major: {} Minor: {} Text: {}'.format(
                        response['error']['errorcode']['major'],
                        response['error']['errorcode']['minor'],
                        response['error']['errormsg'],
                    )
                )
            return response.get('data')
        raise Exception('Fatal error.')

    def _parse_response(self, response):
        """Recursively parse response"""
        result = dict()
        if hasattr(response, 'item'):
            result = self._parse_response(response.item)
        elif hasattr(response, 'key'):
            if isinstance(response.value, str) or \
                    isinstance(response.value, int):
                result = {response.key: response.value}
            else:
                result = {response.key: self._parse_response(response.value)}
        elif isinstance(response, typedArrayType):
            result = list()
            for item in response:
                returned = self._parse_response(item)
                result.append(returned)
        elif isinstance(response, list):
            for item in response:
                returned = self._parse_response(item)
                if isinstance(returned, dict):
                    result = dict(result.items() + returned.items())
        return result
