# -*- coding: utf-8 -*-

"""
Copyright (c) 2013 Petr Jerabek

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

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
        """Command `Login`
        User login to API
        :param username: Username for login
        :param password: Password
        https://soap.subreg.cz/manual/?cmd=Login
        """
        kwargs = {'login': username, 'password': password}
        response = self._request('Login', kwargs)
        self.token = response['ssid']

    def check_domain(self, domain):
        """Command `Check_Domain`
        Check if domain is available or not
        :param domain: Domain for check availability
        https://soap.subreg.cz/manual/?cmd=Check_Domain
        """
        kwargs = {'domain': domain}
        response = self._request('Check_Domain', kwargs)
        if response['avail'] == 1:
            return True
        return False

    def info_domain(self, domain):
        """Command `Info_Domain`
        Get informations about a single domain from your account
        :param domain: Domain name for requested informations
        https://soap.subreg.cz/manual/?cmd=Info_Domain
        """
        kwargs = {'domain': domain}
        response = self._request('Info_Domain', kwargs)
        return response

    def info_domain_cz(self, domain):
        """Command `Info_Domain_CZ`
        Get informations about a single .CZ domain
        :param domain: Domain name for requested informations
        https://soap.subreg.cz/manual/?cmd=Info_Domain_CZ
        """
        kwargs = {'domain': domain}
        response = self._request('Info_Domain_CZ', kwargs)
        return response

    def domains_list(self):
        """Command `Domains_List`
        Get all domains from your account
        :return dict
            :key `domains`: dict of domains
                :key `name`: Domain name
                :key `expire`: Domain expiration date
            :key `count`: Domains count
        https://soap.subreg.cz/manual/?cmd=Domains_List
        """
        return self._request('Domains_List')

    def set_autorenew(self, domain, autorenew):
        """Command `Set_Autorenew`
        Set autorenew policy for your domain.
        By default, domain is deleted when it expire.
        You can set autorenew flag to AUTORENEW, then it will use your credit
        to renew automatically. RENEWONCE will cause renew only for next year.
        :param domain: Registered domain
        :param autorenew: Autorenew setting, allowed values:
            EXPIRE, AUTORENEW, RENEWONCE
        https://soap.subreg.cz/manual/?cmd=Set_Autorenew
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
        """Command `Create_Contact`
        Create contact in Subreg DB
        https://soap.subreg.cz/manual/?cmd=Create_Contact
        """
        raise NotImplementedError

    def update_contact(self, **kwargs):
        """Command `Update_Contact`
        Update contact
        https://soap.subreg.cz/manual/?cmd=Update_Contact
        """
        raise NotImplementedError

    def info_contact(self, contact_id):
        """Command `Info_Contact`
        Get informations about a single contact from your account
        :param contact_id: ID of your querying contact
        https://soap.subreg.cz/manual/?cmd=Info_Contact
        """
        raise NotImplementedError

    def contacts_list(self):
        """Command `Contacts_List`
        Get all contacts from your account
        https://soap.subreg.cz/manual/?cmd=Contacts_List
        """
        return self._request('Contacts_List')

    def check_object(self, _id, _object):
        """Command `Check_Object`
        Check if object is available or not (only CZ,EE)
        :param _id: ID for check availability
        :param _object: contact, nsset, keyset (only CZ, EE)
        https://soap.subreg.cz/manual/?cmd=Check_Object
        """
        raise NotImplementedError

    def info_object(self, _id, _object):
        """Command `Info_Object`
        Info about NIC object (only CZ,EE)
        :param _id: ID for info
        :param _object: contact, nsset, keyset (only CZ, EE)
        https://soap.subreg.cz/manual/?cmd=Info_Object
        """
        raise NotImplementedError

    def make_order(self, **kwargs):
        """Command `Make_Order`
        Create a new order (CreateDomain, ModifyDomain, RenewDomain, ... )
        :arg type:
            https://soap.subreg.cz/manual/?cmd=Create_Domain
            https://soap.subreg.cz/manual/?cmd=Transfer_Domain
            https://soap.subreg.cz/manual/?cmd=AccountTransfer_Domain
            https://soap.subreg.cz/manual/?cmd=TransferApprove_Domain
            https://soap.subreg.cz/manual/?cmd=TransferDeny_Domain
            https://soap.subreg.cz/manual/?cmd=TransferCancel_Domain
            https://soap.subreg.cz/manual/?cmd=SKChangeOwner_Domain
            https://soap.subreg.cz/manual/?cmd=Modify_Domain
            https://soap.subreg.cz/manual/?cmd=ModifyNS_Domain
            https://soap.subreg.cz/manual/?cmd=Delete_Domain
            https://soap.subreg.cz/manual/?cmd=Restore_Domain
            https://soap.subreg.cz/manual/?cmd=Renew_Domain
            https://soap.subreg.cz/manual/?cmd=Backorder_Domain
            https://soap.subreg.cz/manual/?cmd=Preregister_Domain
            https://soap.subreg.cz/manual/?cmd=Create_Object
            https://soap.subreg.cz/manual/?cmd=Transfer_Object
            https://soap.subreg.cz/manual/?cmd=Update_Object
            https://soap.subreg.cz/manual/?cmd=TransferRU_Request
            https://soap.subreg.cz/manual/?cmd=Create_Host
            https://soap.subreg.cz/manual/?cmd=Update_Host
            https://soap.subreg.cz/manual/?cmd=Delete_Host
        https://soap.subreg.cz/manual/?cmd=Make_Order
        """
        raise NotImplementedError

    def info_order(self, order_id):
        """Command `Info_Order`
        Info about existing order
        :param order_id: Order ID
        https://soap.subreg.cz/manual/?cmd=Info_Order
        """
        raise NotImplementedError

    def get_credit(self):
        """Command `Get_Credit`
        Get status of your credit
        https://soap.subreg.cz/manual/?cmd=Get_Credit
        """
        return self._request('Get_Credit')

    def get_accountings(self, from_date, to_date):
        """Command `Get_Accountings`
        Get financial statements from account
        :param from_date: Date (YYYY-mm-dd)
        :param to_date: Date (YYYY-mm-dd)
        https://soap.subreg.cz/manual/?cmd=Get_Accountings
        """
        raise NotImplementedError

    def client_payment(self, username, amount, currency):
        """Command `Client_Payment`
        Add credit to your sub-user. This command WILL generate invoice,
        if you want just correct current amount of credit for any reason,
        please use command Credit_Correction.
        :param username: Login username of the use you want to add credit
        :param amount: Amount of money to add
        :param currency: Currency of added credit
        https://soap.subreg.cz/manual/?cmd=Client_Payment
        """
        raise NotImplementedError

    def credit_correction(self, username, amount, reason):
        """Command `Credit_Correction`
        Correct credit amount of your sub-users. The amount you specify in this
        command will be added to current amount. Use negative values for
        subtracting credit. Please note that currency will depend on
        current user setting.
        :param username: Login username of the user you want to add credit
        :param amount: Amount of money to add/subtract
        :param reason: Human readable reason for this operation
        https://soap.subreg.cz/manual/?cmd=Credit_Correction
        """
        raise NotImplementedError

    def pricelist(self):
        """Command `Pricelist`
        Get pricelist from account
        https://soap.subreg.cz/manual/?cmd=Pricelist
        """
        return self._request('Pricelist')

    def prices(self, tld):
        """Command `Prices`
        Get Prices for TLD from account
        :type tld: Requested TLD
        https://soap.subreg.cz/manual/?cmd=Prices
        """
        raise NotImplementedError

    def get_pricelist(self, pricelist):
        """Command `Get_Pricelist`
        Return all price information in specified pricelist.
        :param pricelist: Identificator of the pricelist you want to download.
        https://soap.subreg.cz/manual/?cmd=Get_Pricelist
        """
        raise NotImplementedError

    def set_prices(self, pricelist, tld, currency, prices=None):
        """Command `Set_Prices`
        Change prices in specified pricelist.
        :param pricelist: Identificator of the pricelist you want to download.
        :param tld: TLD for which you want to change prices.
        :param currency: Currency code the prices use.
        :param prices: List of operations with price
        https://soap.subreg.cz/manual/?cmd=Set_Prices
        """
        raise NotImplementedError

    def download_document(self, document_id):
        """Command `Download_Document`
        Get document information and base64 encoded document that you have
        uploaded or generated on your account.
        :param document_id: Document ID, you can get it in response of
                            `Upload_Document` or by `List_Documents`.
        https://soap.subreg.cz/manual/?cmd=Download_Document
        """
        raise NotImplementedError

    def upload_document(self, name, document, _type=None, filetype=None):
        """Command `Upload_Document`
        Upload document to your account, for use as identification document,
        registration request etc.
        :param name: Filename of the document, including extension
        :param document: base64 encoded document
        :param _type: Type of the document
                     (https://soap.subreg.cz/manual/?cmd=Document_Types)
        :param filetype: MIME type of the file
        https://soap.subreg.cz/manual/?cmd=Upload_Document
        """
        raise NotImplementedError

    def list_documents(self):
        """Command `List_Documents`
        List documents uploaded or generated on your account.
        https://soap.subreg.cz/manual/?cmd=List_Documents
        """
        return self._request('List_Documents')

    def users_list(self):
        """Command `Users_List`
        Retrieve list of all your sub-users
        https://soap.subreg.cz/manual/?cmd=Users_List
        """
        return self._request('Users_List')

    def get_dns_zone(self, domain):
        """Command `Get_DNS_Zone`
        List of DNS records for specified domain.
        :param domain: Registered domain
        https://soap.subreg.cz/manual/?cmd=Get_DNS_Zone
        """
        kwargs = {'domain': domain}
        response = self._request('Get_DNS_Zone', kwargs)
        try:
            return response['records']
        except KeyError:
            return []

    def add_dns_zone(self, domain, template=None):
        """Command `Add_DNS_Zone`
        Add domain to DNS using previously created template.
        :param domain: Registered domain
        :param template: DNS template ID or template name
        https://soap.subreg.cz/manual/?cmd=Add_DNS_Zone
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
        """Command `Delete_DNS_Zone`
        Remove ALL DNS records for specified domain.
        :param domain: Registered domain
        https://soap.subreg.cz/manual/?cmd=Delete_DNS_Zone
        """
        kwargs = {'domain': domain}
        response = self._request('Delete_DNS_Zone', kwargs)
        return response

    def set_dns_zone(self, domain, records):
        """Command `Set_DNS_Zone`
        Specify complete set of records for certain zone.
        Specified records will replace ALL present records.
        :param domain: Registered domain
        :param records: List of dicts of records
        https://soap.subreg.cz/manual/?cmd=Set_DNS_Zone
        """
        raise NotImplementedError

    def add_dns_record(self, domain, record):
        """Command `Add_DNS_Record`
        Add DNS record to zone.
        :param domain: Registered domain
        :param record: dict wirh params:
            `name` Hostname (part of hostname, without registered domain)
            `type` Type of DNS record
            `content` Value of this record (IP address, hostname, text value,..)
            `prio` Priority of this record (MX records only)
            `ttl` TTL value
        https://soap.subreg.cz/manual/?cmd=Add_DNS_Record
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
        """Command `Modify_DNS_Record`
        :param domain: Registered domain
        :param record: dict with ID of existing record
            `id` ID of existing record
            `name` Hostname (part of hostname, without registered domain)
            `type` Type of DNS record
            `content` Value of this record (IP address, hostname, text value,..)
            `prio` Priority of this record (MX records only)
            `ttl` TTL value
        https://soap.subreg.cz/manual/?cmd=Modify_DNS_Record
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
        """Command `Delete_DNS_Record`
        Remove DNS record from zone.
        :param domain: Registered domain
        :param record_id: ID of existing record
        https://soap.subreg.cz/manual/?cmd=Delete_DNS_Record
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
        """Command `POLL_Get`
        Get current poll message
        https://soap.subreg.cz/manual/?cmd=POLL_Get
        """
        return self._request('POLL_Get')

    def poll_ack(self, poll_id):
        """Command `POLL_Ack`
        Ack current poll message
        :param poll_id: POLL ID
        https://soap.subreg.cz/manual/?cmd=POLL_Ack
        """
        raise NotImplementedError

    def oib_search(self, oib):
        """Command `OIB_Search`
        List domains registered for certain OIB, and get the number of domains
        possible to register for this OIB.
        :param oib: Croatian OIB number
        https://soap.subreg.cz/manual/?cmd=OIB_Search
        """
        raise NotImplementedError

    def set_google_mx_records(self, domain):
        """Set Google MX rerods
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
