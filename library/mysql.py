import pymysql


def db_connect():
    db = pymysql.connect(host="数据库地址", user="用户名", password="密码", port=3306, database="数据库名", charset='utf8')
