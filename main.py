from parser.views import *

from datetime import datetime
from time import sleep
from db.views import DB
from echo.views import send_message_chat

s = {
    'Анализ и кодирование информации': '687891',
    'Базы данных': '687892',
    'Объектно-ориентированное программирование': '687894'
}

user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
DB = DB()
while True:
    try:
        subjects = DB.take_subjects()
        students = DB.take_students()

        for i in subjects:
            url = 'https://edu.donstu.ru/Ved/Ved.aspx'

            r = requests.get(url, params={'id': i}, headers={'User-Agent': user_agent})

            soup = BeautifulSoup(r.text, 'html.parser')

            for j in students:
                rating_old = DB.take_rating(j, i)
                rating_new = get_rating(soup, j)

                if rating_new != rating_old[:len(rating_new)]:
                    DB.update_student_rating(j, i, rating_new)
                    subject_name = DB.take_subject_name(i)
                    message = create_message(rating_new, subject_name, DB.take_name(j), DB.take_subjects_args(i))
                    if message:
                        send_message_chat(message)
                    print(transliterate.translit(subject_name, reversed=True),
                          j, datetime.today().strftime("%Y-%m-%d %H.%M.%S")
                          )

        sleep(10)

    except:
        print('Error at', datetime.today().strftime("%Y-%m-%d %H.%M.%S"))
        sleep(120)
