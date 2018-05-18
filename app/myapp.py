from tornado.web import Application

from day5.utils.dbutil import DBUtile


class MyApplication(Application):
    def __init__(self,handlers,tp,sp,um):
        super().__init__(handlers=handlers,template_path=tp,static_path=sp,ui_modules=um)
        self.dbutil = DBUtile()
