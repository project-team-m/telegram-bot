import requests
from bs4 import BeautifulSoup
import transliterate

def create_message(mass, subject_name, name, args):
    res = []

    for i in range(len(args)):
        if mass[i] != '':
            res.append('{}: {}'.format(args[i], mass[i]))

    if res != []:
        message = subject_name + ': ' + name
        for i in res:
            message = '{}\n{}'.format(message, i)
        return message
    else:
        return None

def get_position(soup:BeautifulSoup, n_zach):
    soup = soup.find_all('td', 'dx-al')
    for i in range(len(soup)):
        if soup[i].text == n_zach:
            return i

def get_rating(soup:BeautifulSoup, n_zach):
    soup = soup.find('tr', id='ctl00_MainContent_ucVedBox_TableVed_DXDataRow{}'.format(get_position(soup, n_zach))).find_all('td')
    mass = []

    for i in soup:
        if i.text == '&nbsp;' or i.text == '\xa0':
            mass.append('')
        else:
            mass.append(i.text)

    return tuple(mass)

def get_type_ved(id):
    user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
                  'Gecko/20100101 Firefox/50.0')
    url = 'https://edu.donstu.ru/Ved/Ved.aspx'

    r = requests.get(url, params={'id': id}, headers={'User-Agent': user_agent})

    soup = BeautifulSoup(r.text, 'html.parser')
    if len(get_rating(soup, '1795989')) <= 5:
        return 'Дата сдачи$Оценка в баллах$Оценка'
    else:
        return 'Лек 1$Пр 1$Лаб 1$Пропуски 1$Итог 1$Лек 2$Пр 2$Лаб 2$Пропуски 2$Итог 2$Экзамен$Всего$Оценка$Итоговая оценка$Результат'

def get_ved(group = 32340):
    url = 'https://edu.donstu.ru/Ved/'
    user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
                  'Gecko/20100101 Firefox/50.0')

    r = requests.get(url, params={'group': group}, headers={'User-Agent': user_agent})

    soup = BeautifulSoup(r.text, 'html.parser')

    soup = soup.find_all('tr', 'dxgvDataRow_MaterialCompact')

    mass = []

    for i in soup:

        mass.append((i.find_all('td')[0].text + ' ' + i.find_all('td')[1].text,
                     str(i.find_all('td')[0].find_all('a')[0]).split('=')[-1].split('"')[0],
                     get_type_ved(str(i.find_all('td')[0].find_all('a')[0]).split('=')[-1].split('"')[0])))

    return mass

if __name__ == '__main__':
    for i in get_ved():
        print(i)