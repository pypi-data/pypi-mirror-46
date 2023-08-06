
DepHell Links
=============


.. image:: https://travis-ci.org/dephell/dephell_links.svg?branch=master
   :target: https://travis-ci.org/dephell/dephell_links
   :alt: travis


.. image:: https://ci.appveyor.com/api/projects/status/github/dephell/dephell_links?svg=true
   :target: https://ci.appveyor.com/project/orsinium/dephell-links
   :alt: appveyor


.. image:: https://img.shields.io/pypi/l/dephell-links.svg
   :target: https://github.com/dephell/dephell_links/blob/master/LICENSE
   :alt: MIT License


Parse dependency links.

Installation
------------

Install from `PyPI <https://pypi.org/project/dephell-links/>`_\ :

.. code-block:: bash

   python3 -m pip install --user dephell_links

Usage
-----

.. code-block:: python

   from dephell_links import parse_link

   parse_link('https://github.com/r1chardj0n3s/parse.git')
   # VCSLink(server='github.com', author='r1chardj0n3s', project='parse', vcs='git', protocol='https', user=None, ext='.git', rev=None, name='parse')

   link = parse_link('https://github.com/divio/django-cms/archive/release/3.4.x.zip')
   link
   # URLLink(https://github.com/divio/django-cms/archive/release/3.4.x.zip)
   link.name
   # 'django-cms'

   link = parse_link('./tests/test_parsing.py')
   link
   # FileLink(./tests/test_parsing.py)
   link.name
   # 'test_parsing'
   link.hash
   # 'sha256:ad7927cf442156980659eee391da849e54f472b4bafe20c32cdb242c153528d5'

   link = parse_link('./tests/')
   link
   # DirLink(./tests/)
   link.name
   # 'tests'
