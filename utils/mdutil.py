import hashlib


def mymd5(password):
    m=hashlib.md5()
    m.update(password.encode('utf8'))
    return m.hexdigest()