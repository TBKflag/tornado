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

define('duankou',type=int,default=8001)
parse_config_file('../config/config')


class Blog(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('blog.html',a=100,b=150,rand=self.myfun,posts=[
            {"title":'1',
             'tags':'',
             'author':'jia',
             'content':'第一篇博客',
             "avator":'a.jpg',
             'comment':5},
            {"title": '2',
             'tags': '星座',
             'author': 'jia',
             'avator':None,
             'content': '第一篇博客',
             'comment': 0},
            {"title": '3',
             'tags': 'sex',
             'author': 'jia',
             "avator": 'a.jpg',
             'content': '第一篇博客',
             'comment': 1},
        ])
    # 自定义函数ｍｙｆｕｎ
    def myfun(self, a, b):
        # 生成从ａ到ｂ之间随机一个数
        return randint(a, b)


class BlockModule(UIModule):
    def render(self, *args, **kwargs):
        posts = [
            {"title": '1',
             'tags': '',
             'author': 'jia',
             'content': '第一篇博客',
             "avator": 'a.jpg',
             'comment': 5},
            {"title": '2',
             'tags': '星座',
             'author': 'jia',
             'avator': None,
             'content': '第一篇博客',
             'comment': 0},
            {"title": '3',
             'tags': 'sex',
             'author': 'jia',
             "avator": 'a.jpg',
             'content': '第一篇博客',
             'comment': 1},
        ]
        return self.render_string('mymodule/blog_module.html',posts=posts)




class IndexHandler(RequestHandler):
    def get(self,*args,**kwargs):
        # self.write('my first tornado')
        msg=self.get_query_arguments('msg')
        if msg:
            self.render('login.html', msgage='input error')
        else:
            self.render('login.html', msgage=None)


class LoginHandler(RequestHandler):
    def post(self, *args, **kwargs):
        username=self.get_argument('username')
        password=self.get_argument('password')
        print(username,password)
        # 根据用户输入的用户名和密码，取数据库中查询是否有符合的记录
        # 建立连接．
        password=mymd5(password)
        dbutil=DBUtile()
        if dbutil.login(username,password):
            self.redirect('/blog')
        else:
            self.redirect('/?msg=fail')


class LigubModule(UIModule):
    def render(self, *args, **kwargs):
        # self.request.query　可以获取到ｕｒｌ中的参数
        msg=self.request.query
        if msg:
            return self.render_string('mymodule/login_module.html',msgage='input error')
        return self.render_string('mymodule/login_module.html',msgage='')



class Resign(RequestHandler):
    def get(self,*args,**kwargs):
        self.render('resign.html')

    def post(self,*args,**kwargs):
        username=self.get_body_argument('username')
        password=self.get_body_argument('password')
        city=self.get_body_argument('city')
        if username and password and city:
            avatar=None
            if self.request.files:
                #说明用户上传了头像，将头像保存，头像文件的名称赋值给avator
                file=self.request.files['avatar'][0]
                # 为了防止用户上传的头像文件重名，所以在文件名前增加了时间戳，降低了文件重名概率
                file_name=str(time.time())+file['filename']
                body=file['body']
                writer=open('./mystatics/images/{}'.format(file_name),'wb')
                writer.write(body)
                writer.close()
                avatar=file_name
            # ＭＤ５
            m=hashlib.md5()
            m.update(password.encode('utf8'))
            # 转换为经过ＭＤ５摘要算法处理的密码
            password=m.hexdigest()
            # 写入数据库

            dbutil=DBUtile()
            try:
                dbutil.save(username=username,password=password,city=city,avatar=avatar)
            except Exception as e:
                if str(e)=='参数不完整':
                    raise Exception('参数不完整')
                self.redirect('/resign?msg='+str(e))
        else:
            self.redirect('/resign?msg=empty')



class ResignModule(UIModule):
    def render(self,*args,**kwargs):
        r=''
        q=self.request.query
        #msg=empty
        #msg=dberror
        #msg=duplicate
        if q:
            q=q.split('=')[1]
            if q=='empty':
                r='注册信息为空'
            if q=='dberror':
                r='数据库错误'
            if q=='duplicate':
                r='用户名重复'
        return self.render_string('mymodule/resign_module.html',result=r)


app=MyApplication([('/',IndexHandler),
                 ('/login/(a-z0-9A-Z)*',LoginHandler),
                 ('/blog',Blog),
                 ('/resign',Resign)],
                tp='./mytemplate',
                sp='./mystatics',
                um={'loginmodule':LigubModule,'blogmodule':BlockModule,'resignmodule':ResignModule})
server=HTTPServer(app)
server.listen(options.duankou)
IOLoop.current().start()

