import pymysql


class DBUtile():
    def __init__(self,**kwargs):
        host=kwargs.get('host','127.0.0.1')
        port=kwargs.get('port',3306)
        user=kwargs.get('user','root')
        password=kwargs.get('password','123456')
        database=kwargs.get('database','blogdb')
        charset=kwargs.get('charset','utf8')

        setting={'host':host,'port':port,'user':user,'password':password,'database':database,'charset':charset}

        db=pymysql.connect(**setting)
        if db:
            self.cursor=db.cursor()
        else:
            raise Exception('数据库异常')

    def login(self,username,password):
        sql='select count(*) from tb_user where user_name=%s and user_password=%s'
        params=(username,password)
        self.cursor.execute(sql,params)
        result=self.cursor.fetchone()
        if result[0]:
            return True
        else:
            return False

    def save(self,**kwargs):
        username=kwargs.get('username',None)
        password=kwargs.get('password',None)
        city=kwargs.get('city',None)
        avatar=kwargs.get('avatar',None)

        if username and password and city:
            sql='insert into tb_user(user_name, user_password, user_avatar, user_city) VALUES (%s,%s,%s,%s)'
            params=(username,password,avatar,city)
            try:
                self.cursor.execute(sql,params)
                self.cursor.connection.commit()
                return True
            except Exception as e:
                msg='dberror'
                info = str(e)
                err_code = info.split(',')[0].split('(')[1]
                if err_code == '1062':
                    msg='duplicate'
                raise Exception(msg)
        else:
            raise Exception('参数不完整')

