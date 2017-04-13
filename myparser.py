from bs4 import BeautifulSoup
import re
import requests

def check_typos(request):
    """
    Эта функция позволит проверить не опечатался ли пользователь.
    :param request: string
    :return: string

    """
    # Получим поисковую страницу
    url = 'http://www.google.com/search?q='
    page = requests.get(url + request.lower()) # Делаем запрос

    # Сделаем из сьраницы суп и распарсим ее.
    soup = BeautifulSoup(page.text, "html.parser")
    raw = soup.find_all("a", class_="spell")

    # С помощью регулярных выражений сотавляем только запрос.
    new_name = re.sub(u'[^А-Яа-я\s]*', u'', str(raw[0]))
    print(new_name)
print(check_typos("Fkbrcfylh Ytdcrbq"))