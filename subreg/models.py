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


class BaseModel(object):
    """Implement custom __init__ method"""

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)


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
