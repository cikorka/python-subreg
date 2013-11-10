# -*- coding: utf-8 -*-


class BaseModel(object):
    """Implement custom __init__ method"""

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


class DNSRecord(BaseModel):
    """Represent DNS Record"""

    id = None
    """ID of existing record"""
    name = None
    """Hostname (part of hostname, without registered domain)"""
    type = None
    """Type of DNS record"""
    content = None
    """Value of this record (IP address, hostname, text value etc.)"""
    prio = None
    """Priority of this record (MX records only)"""
    ttl = None
    """TTL value"""


class Contact(BaseModel):
    """Represent Contact
    One of the id, regid or new is REQUIRED !
    https://soap.subreg.cz/manual/?cmd=Type_Contact
    """

    id = None
    """ID from Subreg.DB (G-xxxxxx)"""
    regid = None
    """ID from Registry (CZ-NIC ID, SK-NIC ID, etc ...)"""
    name = None
    """First name of contact"""
    surname = None
    """Second name of contact"""
    org = None
    """Organization name (optionally)"""
    street = None
    """Address of contact"""
    city = None
    """City of contact"""
    pc = None
    """ZIP code of contact"""
    sp = None
    """State of contact (optionally)"""
    cc = None
    """ISO Country Code of contact"""
    phone = None
    """Phone of contact in format +1.234567890"""
    fax = None
    """Faxsimile of contact in format +1.234567890 (optionally)"""
    email = None
    """Email of contact"""
