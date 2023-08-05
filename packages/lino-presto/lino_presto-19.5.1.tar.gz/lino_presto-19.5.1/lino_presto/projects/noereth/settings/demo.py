import datetime
from ..settings import *
class Site(Site):
    languages = "de fr en"
    is_demo_site = True
    the_demo_date = datetime.date(2017, 3, 12)
#    default_ui = 'lino_react.react'
#    default_ui = 'lino_extjs6.extjs'

    # def setup_plugins(self):
    #     super(Site, self).setup_plugins()
    #     self.plugins.ledger.configure(start_year=2017)
    #     # print "20151217 a", hash(self.plugins.ledger)

    
SITE = Site(globals())

DEBUG = True
