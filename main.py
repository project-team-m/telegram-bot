from datetime import datetime
from time import sleep
from models import DB
from views import *
from parser_dgtu import *
from log.loging import Log

s = {
    'Анализ и кодирование информации': '687891',
    'Базы данных': '687892',
    'Объектно-ориентированное программирование': '687894'
}

user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
DB = DB()
log = Log('Telegram')
logs = 0
while True:
    try:
        DB.connect()
        subjects = DB.take_subjects()
        students = DB.take_students()

        for i in subjects:
            logs += 1
            url = 'https://edu.donstu.ru/Ved/Ved.aspx'

            r = requests.get(url, params={'id': i}, headers={'User-Agent': user_agent})

            if r.status_code == 200:
                if logs % 100 == 0:
                    log.write_log('Connect site')
                soup = BeautifulSoup(r.text, 'html.parser')

                for j in students:
                    rating_old = DB.take_rating(j, i)
                    rating_new = get_rating(soup, j)

                    if rating_new != rating_old[:len(rating_new)] and len(rating_new) > 2:
                        DB.update_student_rating(j, i, rating_new)
                        subject_name = DB.take_subject_name(i)
                        message = create_message(rating_new, subject_name, DB.take_name(j),
                                                 DB.take_subjects_args(i))

                        log.write_actions_log('Send {}: {}, '.format(subject_name, DB.take_name(j), rating_new))
                        if message:
                            send_message_chat(message)
                        print(transliterate.translit(subject_name, reversed=True),
                              j,
                              datetime.today().strftime("%Y-%m-%d %H.%M.%S")
                              )
            else:
                log.write_log('Status code = {}'.format(r.status_code))
        DB.close()
        sleep(10)

    except requests.exceptions.HTTPError:
        log.write_error_log('HTTPError')
        print('Error at', datetime.today().strftime("%Y-%m-%d %H.%M.%S"), 'HTTPError')
        sleep(120)

    except requests.exceptions.ConnectionError:
        log.write_error_log('ConnectionError')
        print('Error at', datetime.today().strftime("%Y-%m-%d %H.%M.%S"), 'ConnectionError')
        sleep(120)

    except requests.exceptions.Timeout:
        log.write_error_log('Timeout from site')
        print('Error at', datetime.today().strftime("%Y-%m-%d %H.%M.%S"), 'Timeout')
        sleep(120)

    except:
        log.write_error_log('Wtf what is it')
        print('Error at', datetime.today().strftime("%Y-%m-%d %H.%M.%S"), 'Timeout')
        sleep(120)
