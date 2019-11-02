from parser.views import *
import transliterate
from datetime import datetime
from time import sleep

s = {
    'Анализ и кодирование информации': 687891,
    'Базы данных': 687892,
    'Объектно-ориентированное программирование': 687894
}

#Сань, запиши это в первую строку в бд
output = ['Лек 1', 'Пр 1', 'Лаб 1', 'Пропуски 1', 'Итог 1', 'Лек 2', 'Пр 2', 'Лаб 2', 'Пропуски 2', 'Итог 2', 'Экзамен',
          'Всего', 'Оценка', 'Итоговая оценка']

while True:
    try:
        #subjects = take_subjects()
        subjects = (s[i] for i in s)
        #students = take_students()
        students = (1774783, 1795989, 1725313)

        for i in subjects:
            url = 'https://edu.donstu.ru/Ved/Ved.aspx'

            params = {'id': i}
            r = requests.get(url, params=params)

            lines = r.text

            for j in students:
                #rating_old = take_rating(j)
                rating_old = ('14', '', '', '', '14', '', '', '', '', '', '', '14', 'Неуд', 'Н/я')
                rating_new = take_rating(j, lines)

                if rating_new != rating_old:
                    #update_student_rating(j, rating_new)
                    #subject_name = take_subject_name()
                    subject_name = 'Базы данных'
                    message = create_message(rating_new, output, subject_name)
                    #send_message_chat(message)
                    print(transliterate.translit(subject_name, reversed=True),
                          j, datetime.today().strftime("%Y-%m-%d %H.%M.%S")
                          )

        sleep(10)

    except:
        print('Error at', datetime.today().strftime("%Y-%m-%d %H.%M.%S"))
        sleep(120)