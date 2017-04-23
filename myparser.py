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

def books(name_of_writer, name_of_book):
    """
    Эта функция возвращает нам строку из нудной книги.
    :param writers: sting
    :param name_of_book: string
    :param page: int
    :param line: int
    """
    #Словарь найденных книг.
    books = {}

    # Парсим сайт.
    url = 'http://knijky.ru/search?search_api_views_fulltext='
    page = requests.get(url + name_of_book.lower())

    # Сделаем из страницы суп и распарсим ее.
    soup = BeautifulSoup(page.text, "html.parser")
    raw_books = soup.find_all("div", class_="views-field views-field-title")
    raw_writers = soup.find_all("div", class_="views-field views-field-field-author-fio")

    for book, writer in zip(raw_books, raw_writers):
        tmp1_books = str(book).split('a href="/')
        tmp2_books = tmp1_books[1].split('">')
        tmp1_writers = str(writer).split('a href="/')
        tmp2_writers = tmp1_writers[1].split('">')
        tmp = name_of_writer.split(" ")

        if (tmp2_books[1].lower().find(name_of_book.lower()) != -1):
            name_writers = re.sub(u'[^А-Яа-я1-9\s]*', u'',
                                  tmp2_writers[1].lstrip())

            if (name_writers.lower().find(tmp[0].lower()) != -1) and \
                    (name_writers.lower().find(tmp[1].lower()) != -1):
                name_books = re.sub(u'[^А-Яа-я1-9\s]*', u'',
                                    tmp2_books[1].lstrip())
                books[name_books] = "http://knijky.ru/" + tmp2_books[0]

    return(books)