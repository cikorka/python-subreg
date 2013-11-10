# -*- coding: utf-8 -*-

from collections import namedtuple

DNSRecord = namedtuple('DNSRecord', ['name', 'type', 'content', 'prio', 'ttl'])

Contact = namedtuple('Contact', [
    'id', 'regid', 'name', 'surname', 'org', 'street', 'city', 'pc', 'sp', 'cc',
    'phone', 'fax', 'email'
])
"""
:arg id ID from Subreg.DB (G-xxxxxx)
:arg regid ID from Registry (CZ-NIC ID, SK-NIC ID, etc ...)
:arg name First name of contact
:arg surname Second name of contact
:arg org Organization name (optionally)
:arg street Address of contact
:arg city City of contact
:arg pc ZIP code of contact
:arg sp State of contact (optionally)
:arg cc ISO Country Code of contact
:arg phone Phone of contact in format +1.234567890
:arg fax Faxsimile of contact in format +1.234567890 (optionally)
:arg email Email of contact
One of the id, regid or new is REQUIRED !
https://soap.subreg.cz/manual/?cmd=Type_Contact
"""
