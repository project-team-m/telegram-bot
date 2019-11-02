import requests
import sqlite3

#from echo.config import HOME_DIR

def create_db():
    #CREATE TABLE students(id INTEGER PRIMARY KEY AUTOINCREMENT, n_zach INTEGER);
    """CREATE TABLE subjects(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name VARCHAR(50),
    id_site INTEGER
    );"""
    """#CREATE TABLE rating(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_student INTEGER,
    id_subject INTEGER,
    lec_1 VARCHAR(10),
    pr_1 VARCHAR(10),
    lab_1 VARCHAR(10),
    skip_1 VARCHAR(10),
    result_1 VARCHAR(10),
    lec_2 VARCHAR(10),
    pr_2 VARCHAR(10),
    lab_2 VARCHAR(10),
    skip_2 VARCHAR(10),
    result_2 VARCHAR(10),
    exam VARCHAR(10),
    all_point VARCHAR(10),
    oc VARCHAR(10),
    result_oc VARCHAR(10),
    FOREIGN KEY(id_student) REFERENCES students(id),
    FOREIGN KEY(id_subject) REFERENCES subjects(id)
    );"""
    pass

def insert_student(n_zach):
    conn = sqlite3.connect("{}/main.db".format(HOME_DIR))
    cursor = conn.cursor()

    cursor.execute("INSERT INTO students(n_zach) VALUES(?)", (n_zach, ))

    conn.commit()

def insert_subject(name, id_site):
    conn = sqlite3.connect("../main.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO subjects(name, id_site) VALUES(?, ?)", (name, id_site))

    conn.commit()

def insert_rating(id_student, id_subject):
    pass

def take_rating(student ,lines):
    return tuple(take_results(
                       lines[lines.find('ctl00_MainContent_ucVedBox_TableVed_DXDataRow{}'.format(find_position_in_site(str(student), lines) - 1))::].split('">')[2:16]
                      ))

def take_results(string):
    mass = []
    for i in string:
        znach = i.split('<')[0]
        if znach == '&nbsp;':
            mass.append('')
        else:
            mass.append(znach)
    return mass

def create_message(arg, mass, subject_name):
    res = []
    for i in range(len(arg)):
        if mass[i] != '':
            res.append('{} {}'.format(arg[i], mass[i]))

    message = subject_name
    for i in res:
        message = '{}\n{}'.format(message, i)

    return res

def find_position_in_site(id_book, lines):
    try:
        return int(lines[:lines.find(id_book)].split('<td class=')[-2].split('</td>')[0].split('>')[1])
    except:
        return False


if __name__ == '__main__':
    '''peyload = {'id': 687891}
    url = 'https://edu.donstu.ru/Ved/Ved.aspx'

    r = requests.get(url, params=peyload)
    lines = r.text
    num = find_position_in_site('1795989', lines)
    print(take_results(
                       lines[lines.find('ctl00_MainContent_ucVedBox_TableVed_DXDataRow{}'.format(num - 1))::].split('">')[2:16]
                      )
         )
    '''
    a = {
        'Анализ и кодирование информации': 687891,
        'Базы данных': 687892,
        'Объектно-ориентированное программирование': 687894,
        'Операционные системы': 687896,
        'Программирование под платформу .NET': 687897,
        'Сети и телекоммуникации': 687898
    }
    for i in a:
        insert_subject(i, a[i])