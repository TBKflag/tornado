import hashlib
from uuid import uuid4


def mymd5(password):
    m=hashlib.md5()
    m.update(password.encode('utf8'))
    return m.hexdigest()

def myuuid():
    #可直接生成一个４０位的字符串
    u = uuid4()
    m=hashlib.md5()
    m.update(u.bytes)
    return m.hexdigest()