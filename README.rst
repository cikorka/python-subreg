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

- Get DNS Zone for domain

  >>> records = subreg.get_dns_zone('example.com')

- Add DNS record to domain DNS zone

  >>> record = dict(name='', type='TXT', content='content')
  >>> record_id = subreg.add_dns_record('example.com', record)

- Set Google MX records

  >>> subreg.set_google_mx_records('example.com')


`Subreg API documentation <https://soap.subreg.cz/manual/>`_
