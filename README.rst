Python wrapper around the subreg.cz SOAP API

Install
-------
.. code:: bash

    pip install python-subreg

Using
-----
First import module and instance class

>>> from subreg import Api
>>> subreg = Api('username', 'password')

- Get informations about a single domain from your account

  >>> domain_info = subreg.info_domain('example.com')
  >>> print domain_info

- Get DNS Zone for domain

  >>> records = subreg.get_dns_zone('example.com')

- Add DNS record to domain DNS zone

  >>> record = dict(name='', type='TXT', content='content')
  >>> record_id = subreg.add_dns_record('example.com', record)
  >>> print record_id

- Set Google MX records

  >>> subreg.set_google_mx_records('example.com')


- `python-subreg documentation <http://python-subreg.readthedocs.org/en/latest/>`_
- `Subreg API documentation <https://soap.subreg.cz/manual/>`_
