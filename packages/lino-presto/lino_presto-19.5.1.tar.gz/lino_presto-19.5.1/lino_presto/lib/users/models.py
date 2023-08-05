# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from lino.modlib.users.models import *

from lino.api import _


class User(User):
    
    class Meta(User.Meta):
        abstract = dd.is_abstract_model(__name__, 'User')
        
