import pymysql.cursors


class BD:
    def __init__(self):
        self.mydb = pymysql.connect(
            host='62.109.15.226',
            user='user_1',
            password='password',
            db='test')

    def CreateWe(self):
        with self.mydb.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS We
            (
          ID    INT         NOT NULL AUTO_INCREMENT,
          Nzach INT         NOT NULL,
          Fam   VARCHAR(30) NOT NULL,
          PRIMARY KEY (ID)
      );''')

a = BD()

a.CreateWe()