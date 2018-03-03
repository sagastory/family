#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

import sys     #utf-8，兼容汉字
reload(sys)
sys.setdefaultencoding("utf-8")

from handlers.indexhandler import IndexHandler  
from handlers.indexhandler import GetrelaHandler  
from handlers.familyhandler import FamilyHandler
from handlers.createhandler import CreateHandler
from handlers.createhandler import writeCommentHandler
from handlers.createhandler import writeMsgHandler
from handlers.createhandler import writeTxtHandler
from handlers.createhandler import addMemberHandler
from handlers.createhandler import addFinishHandler
from handlers.loginhandler import LoginHandler
from handlers.loginhandler import PersonHandler
from handlers.loginhandler import LogoutHandler
from handlers.loginhandler import InvoteHandler

url = [
    (r'/', IndexHandler),
    (r'/getrela', GetrelaHandler),
    (r'/family/(?P<fid>.*)', FamilyHandler),
    (r'/family', FamilyHandler),
    (r'/addfinish', addFinishHandler),
    (r'/create', CreateHandler),
    (r'/addmember', addMemberHandler),
    (r'/writecomment',writeCommentHandler),
    (r'/writetxt',writeTxtHandler),
    (r'/writemsg',writeMsgHandler),
    (r'/login', LoginHandler),
    (r'/person/(?P<pid>.*)', PersonHandler),
    (r'/invote/(?P<fid>.*)/(?P<phone>.*)', InvoteHandler),
    (r'/invote', InvoteHandler),
    (r'/logout', LogoutHandler),
    (r'/register', LoginHandler)
]