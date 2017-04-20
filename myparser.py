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
    page = requests.get(url + request.lower())

    # Сделаем из сnраницы суп и распарсим ее.
    soup = BeautifulSoup(page.text, "html.parser")
    raw = soup.find_all("a", class_="spell")

    if raw == []:
        return request

    # С помощью регулярных выражений сотавляем только запрос.
    new_name = re.sub(u'[^А-Яа-я\s]*', u'', str(raw[0])).lstrip()
    return(new_name.title())

def books(writers, name_of_book, page, line):
    """
    Эта функция возвращает нам строку из нудной книги.
    :param writers: sting
    :param name_of_book: string
    :param page: int
    :param line: int
    :return: string
    """
    # Массив возможных электронных библиотек
    library = [
        "http://online-knigi.com/search/books?text=",
        "http://knijky.ru/search?search_api_views_fulltext=",
        "http://rubook.org/search.php?searchterm=~&searchtype=Найти"
    ]

    for url in library:
        page = requests.get(url + name_of_book.lower())

        soup = BeautifulSoup(page.text, "html.parser")
        raw = soup.find_all("a", class_="href")

