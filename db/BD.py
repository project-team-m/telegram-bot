import pymysql.cursors

from parser.views import get_ved

class BD:
    def __init__(self):
        self.mydb = pymysql.connect(
            host='62.109.15.226',
            user=,
            password=,
            db='test')

    def create_students(self):
        with self.mydb.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS students
                (
                    id    INT PRIMARY KEY AUTO_INCREMENT,
                    n_zach VARCHAR(30) NOT NULL,
                    name VARCHAR(30) NOT NULL
                );''')

    def create_subjects(self):
        with self.mydb.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subjects(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    id_site VARCHAR(30) NOT NULL,
                    columns VARCHAR(1000) NOT NULL,
                    flag INT NOT NULL DEFAULT 1
                );''')

    def create_ved(self):
        with self.mydb.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ved(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    id_student INT,
                    id_subject INT,
                    col1 VARCHAR(50),
                    col2 VARCHAR(50),
                    col3 VARCHAR(50),
                    col4 VARCHAR(50),
                    col5 VARCHAR(50),
                    col6 VARCHAR(50),
                    col7 VARCHAR(50),
                    col8 VARCHAR(50),
                    col9 VARCHAR(50),
                    col10 VARCHAR(50),
                    col11 VARCHAR(50),
                    col12 VARCHAR(50),
                    col13 VARCHAR(50),
                    col14 VARCHAR(50),
                    col15 VARCHAR(50),
                    FOREIGN KEY(id_student)
                    REFERENCES students(id),
                    FOREIGN KEY(id_subject)
                    REFERENCES subjects(id)
                );''')

    def create_db(self):
        self.create_students()
        self.create_subjects()
        self.create_ved()

    def insert_subjects(self):
        with self.mydb.cursor() as cursor:
            subject = get_ved()
            for i in subject:
                cursor.execute('''
                    INSERT INTO subjects(name, id_site, columns)
                    VALUES
                    (%s, %s, %s)
                ''', i)

a = BD()
a.create_db()
a.insert_subjects()
