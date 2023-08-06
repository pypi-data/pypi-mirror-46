# coding=utf-8
# pylint: disable=broad-except, import-error
import pymysql as mysql



class SqlConnection(object):

    def __init__(self, host="172.29.130.138", port=3306, user="test001", passwd="Cnex!2020", db_name="production_test"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.conn = mysql.connect(host=self.host, port=self.port, user=self.user,
                                  passwd=self.passwd, db=self.db_name, charset="utf8")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_result(self, key):
        cmd = "SELECT * FROM test_results WHERE test_key='{}'".format(key)
        self.cursor.execute(cmd)
        result = self.cursor.fetchone()
        return result
