# 手动设置ｓｅｓｓｉｏｎ
'''
{身份标示:{k1=v1,k2=v2},
身份标示２:{k1=v1,k2=v2},
}
'''
from day5.utils.mdutil import myuuid

session={}
class Session():
    # 这种方法只能由Ｐｙｔｈｏｎ解释器调用
    def __init__(self,handler):
        self.handler=handler
    def __getitem__(self, key):
        # 获取这次访问浏览器时，cookie记录的访问者的身份信息
        uid=self.handler.get_cookie('uid')
        if uid:
            d = session.get(uid,None)
            if d:
                return d.get(key,None)
            else:
                return None
        else:
            return None
    def __setitem__(self, key, value):
        uid=self.handler.get_cookie('uid')
        if uid:
            d=session.get(uid,None)
            if d:
                d[key]=value
            else:
                a={}
                a[key]=value
                session[uid]=a
        else:
            a={}
            a[key]=value
            uid=myuuid()
            session[uid]=a
            self.handler.set_cookie('uid',id,expires_days=30)