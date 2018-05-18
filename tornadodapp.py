import hashlib
from os import remove
from random import randint

import time
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define,parse_config_file,options
from tornado.web import Application, RequestHandler, UIModule
import pymysql

from day.utils.dbutil import DBUtile
from day.utils.mdutil import *
from day5.app.myapp import MyApplication
from day5.app.myhandler import IndexHandler, LoginHandler, Blog, Resign, Checkhandler, Headpic
from day5.app.mymodule import LigubModule, BlockModule, ResignModule
from day5.app.mysettings import setting

# define('duankou',type=int,default=8001)
# parse_config_file('../config/config')




app=MyApplication([('/',IndexHandler),
                 ('/login/(a-z0-9A-Z)*',LoginHandler),
                 ('/blog',Blog),
                 ('/resign',Resign),
                 ('/check',Checkhandler),
                 ],
                tp='./mytemplate',
                sp='./mystatics',
                um={'loginmodule':LigubModule,'blogmodule':BlockModule,'resignmodule':ResignModule})
server=HTTPServer(app)
server.listen(setting['duankou'])
IOLoop.current().start()

