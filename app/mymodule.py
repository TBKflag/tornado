from tornado.web import UIModule


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


class LigubModule(UIModule):
    def render(self, *args, **kwargs):
        # self.request.query　可以获取到ｕｒｌ中的参数
        msg=self.request.query
        if msg:
            return self.render_string('mymodule/login_module.html',msgage='input error')
        return self.render_string('mymodule/login_module.html',msgage='')


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