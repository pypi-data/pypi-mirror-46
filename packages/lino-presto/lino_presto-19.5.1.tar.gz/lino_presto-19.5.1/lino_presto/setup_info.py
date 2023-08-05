# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# Note that this module may not have a docstring because any
# global variable defined here will override the global
# namespace of lino/__init__.py who includes it with execfile.

# This module is part of the Lino test suite.
# To test just this module:
#
#   $ python setup.py test -s tests.PackagesTests

from __future__ import unicode_literals

SETUP_INFO = dict(
    name='lino_presto',
    version='19.5.1',
    install_requires=['lino_xl'],
    tests_require=[],

    description="A Lino application for managing services",
    license='BSD License',
    include_package_data=True,
    zip_safe=False,
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://presto.lino-framework.org",
    #~ test_suite = 'lino.test_apps',
    test_suite='tests',
    classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2
  Development Status :: 4 - Beta
  Environment :: Web Environment
  Framework :: Django
  Intended Audience :: Developers
  Intended Audience :: System Administrators
  License :: OSI Approved :: BSD License
  Natural Language :: English
  Natural Language :: French
  Natural Language :: German
  Operating System :: OS Independent
  Topic :: Database :: Front-Ends
  Topic :: Home Automation
  Topic :: Office/Business""".splitlines())

SETUP_INFO.update(long_description="""\

Lino Presto is an application for managing services with physical
on-site presence of the workers.  For organisations where calendar
entries are the base for writing invoices.  Services can be
individually scheduled or recurring calendar entries based on
contracts.  Integrated calendar and contacts.  Automatically generate
invoices.  Optional functionalities include accounting (payments,
purchases, general ledger, VAT declarations).

- The central project homepage is http://presto.lino-framework.org

- German documentation is at http://de.presto.lino-framework.org/

- For *introductions* and *commercial information* about Lino Presto
  see http://www.saffre-rumma.net
  
The name "Presto" originally comes from "prestations de service", the
French expression for service providements.  It also means "quick" in
Italian.

""")

SETUP_INFO.update(packages=[str(n) for n in """
lino_presto
lino_presto.lib
lino_presto.lib.contacts
lino_presto.lib.contacts.fixtures
lino_presto.lib.cal
lino_presto.lib.cal.fixtures
lino_presto.lib.invoicing
lino_presto.lib.invoicing.fixtures
lino_presto.lib.ledger
lino_presto.lib.ledger.fixtures
lino_presto.lib.orders
lino_presto.lib.presto
lino_presto.lib.presto.fixtures
lino_presto.lib.products
lino_presto.lib.sales
lino_presto.lib.sales.fixtures
lino_presto.lib.users
lino_presto.lib.users.fixtures
lino_presto.projects
lino_presto.projects.noereth
lino_presto.projects.noereth.settings
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino_presto': [
        ('**/sandbox/**',        'ignore', None),
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**/linoweb.js',        'jinja2', None),
        #~ ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
        #~ ('**/templates/**.txt',  'genshi', {
        #~ 'template_class': 'genshi.template:TextTemplate'
        #~ })
    ],
})

SETUP_INFO.update(package_data=dict())
