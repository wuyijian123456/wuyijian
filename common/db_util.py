import pymysql
from pymysql.cursors import DictCursor
from config.settings import DB_CONFIG
from core.logger import log
class DBUtil:
    _instance = None
    def __new__(cls):
     if cls._instance is None:
         cls._instance = super().__new__(cls)
         cls._instance.conn = pymysql.connect(**DB_CONFIG, charset="utf8mb4")
         cls._instance.cursor = cls._instance.conn.cursor(DictCursor)
     return cls._instance
    def query(self, sql,params=None):
     self.cursor.execute(sql,params or ())
     return self.cursor.fetchall()
    def execute(self, sql,params=None):
     self.cursor.execute(sql,params or ())
     self.conn.commit()
    def close(self):
     self.cursor.close()
     self.conn.close()
db = DBUtil()