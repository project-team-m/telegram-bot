import pymysql.cursors


from parser.views import get_ved
from db.config import *


class DB:
    def connect(self):
        self.mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db)

    def close(self):
        self.mydb.close()

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
                    col1 VARCHAR(500) DEFAULT '',
                    col2 VARCHAR(500) DEFAULT '',
                    col3 VARCHAR(500) DEFAULT '',
                    col4 VARCHAR(500) DEFAULT '',
                    col5 VARCHAR(500) DEFAULT '',
                    col6 VARCHAR(500) DEFAULT '',
                    col7 VARCHAR(500) DEFAULT '',
                    col8 VARCHAR(500) DEFAULT '',
                    col9 VARCHAR(500) DEFAULT '',
                    col10 VARCHAR(500) DEFAULT '',
                    col11 VARCHAR(500) DEFAULT '',
                    col12 VARCHAR(500) DEFAULT '',
                    col13 VARCHAR(500) DEFAULT 'Неуд',
                    col14 VARCHAR(500) DEFAULT 'Н/я',
                    col15 VARCHAR(500) DEFAULT 'Н/я',
                    FOREIGN KEY(id_student)
                    REFERENCES students(id),
                    FOREIGN KEY(id_subject)
                    REFERENCES subjects(id)
                );''')

    def create_db(self):
        self.create_students()
        self.create_subjects()
        self.create_ved()
        for i in students_template:
            self.insert_student(i[0], i[1])
        self.insert_subjects()

    def insert_student(self, n_zach, name):
        with self.mydb.cursor() as cursor:
            subjects = get_ved()

            sql = '''INSERT INTO students(n_zach, name)
                     VALUES
                     (%s, %s);'''

            cursor.execute(sql, (n_zach, name,))

            self.mydb.commit()

    def insert_subjects(self):
        with self.mydb.cursor() as cursor:
            subjects = get_ved()

            sql = '''SELECT id FROM students;'''
            cursor.execute(sql)
            students = cursor.fetchall()

            sql = '''INSERT INTO subjects(name, id_site, columns)
                     VALUES
                     (%s, %s, %s);'''

            cursor.executemany(sql, subjects)
            self.mydb.commit()

            sql = '''SELECT id FROM subjects WHERE flag = 1;'''
            cursor.execute(sql)
            subjects = cursor.fetchall()

            sql = '''INSERT INTO ved(id_student, id_subject)
            VALUES (%s, %s);'''

            for subject in subjects:
                for student in students:
                    cursor.execute(sql, (student, subject,))


            self.mydb.commit()

    def change_normal(self, obj):
        mass = []
        for i in obj:
            mass.append(i[0])
        return mass

    def take_students(self):
        with self.mydb.cursor() as cursor:
            sql = '''SELECT n_zach FROM students;'''

            cursor.execute(sql)

            return self.change_normal(cursor.fetchall())

    def take_subjects(self):
        with self.mydb.cursor() as cursor:
            sql = '''SELECT id_site FROM subjects;'''

            cursor.execute(sql)

            return self.change_normal(cursor.fetchall())

    def take_rating(self, student, subject):
        with self.mydb.cursor() as cursor:
            sql = '''SELECT col1, col2, col3, col4, col5, col6, col7,
             col8, col9, col10, col11, col12, col13, col14, col15 FROM ved
             WHERE id_student = (SELECT id FROM students WHERE n_zach = %s) AND
             id_subject = (SELECT id FROM subjects WHERE id_site = %s);'''

            cursor.execute(sql, (student, subject,))

            return cursor.fetchone()

    def update_student_rating(self, student, subject, mass):
        with self.mydb.cursor() as cursor:
            if len(mass) == 15:
                sql = '''UPDATE ved
                SET col1 = %s, col2 = %s, col3 = %s, col4 = %s, col5 = %s, col6 = %s, col7 = %s,
                 col8 = %s, col9 = %s, col10 = %s, col11 = %s, col12 = %s, col13 = %s, col14 = %s, col15 = %s
                 WHERE id_student = (SELECT id FROM students WHERE n_zach = %s) AND
                 id_subject = (SELECT id FROM subjects WHERE id_site = %s);'''
            else:
                sql = '''UPDATE ved
                                SET col1 = %s, col2 = %s, col3 = %s, col4 = %s, col5 = %s
                                 WHERE id_student = (SELECT id FROM students WHERE n_zach = %s) AND
                                 id_subject = (SELECT id FROM subjects WHERE id_site = %s);'''

            cursor.execute(sql, mass + (student,) + (subject,))

            self.mydb.commit()

    def take_subject_name(self, subject):
        with self.mydb.cursor() as cursor:
            sql = '''SELECT name FROM subjects WHERE id_site = %s;'''

            cursor.execute(sql, subject)

            return cursor.fetchone()[0]

    def take_name(self, student):
        with self.mydb.cursor() as cursor:
            sql = '''SELECT name FROM students WHERE n_zach = %s;'''

            cursor.execute(sql, student)

            return cursor.fetchone()[0]

    def take_subjects_args(self, subject):
        with self.mydb.cursor() as cursor:
            sql = '''SELECT columns FROM subjects WHERE id_site = %s;'''

            cursor.execute(sql, subject)

            return cursor.fetchone()[0].split('$')

if __name__ == '__main__':
    a = DB()

    a.create_db()