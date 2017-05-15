import classclient
import myconst
import myparser
import numpy
import random
import telebot

TOKEN = '304243519:AAGRSN21G8Ft0eO5QBKlf79-q-dpSnzjrJA'
bot = telebot.TeleBot(TOKEN)

def chat():
    clients = {}
    all_writers = myparser.find_all_writers()

    def start_bot():
        # Заставим бота "висеть" и ждать команды.
        bot.polling(none_stop=True)

    @bot.message_handler(commands=['start'])
    def start_handler(message):

        # Занесем клиентов в базу.
        chat_id = message.chat.id
        client = classclient.Client(chat_id)
        clients[message.chat.id] = client

        message_for_client = "Здравствуйте, я бот, который гадает по книгам.\n" \
                             "Для начала, вам стоит вызвать команду /help и " \
                             "посмотреть все мои инструкции!\nХороших предсказаний!\n"
        chat_id = message.chat.id
        bot.send_message(chat_id, message_for_client)

    @bot.message_handler(commands=['help'])
    def help_handler(message):
        chat_id = message.chat.id

        message_for_client = 'Список команд для бота:\n' \
        '/start - начать предсказание\n' \
        '/choose_writer "Имя" "Фамилия" - выбрать автора\n' \
        '/choose_book "Название" - выбрать название книги\n' \
        '/get_k_random_books - получить k случайных книг выбранного автора\n' \
        '/choose_page - выбрать страницу\n' \
        '/get_random_page - получить рандомную страницу\n' \
        '/choose_line - выбрать строку\n' \
        '/get_random_line - получить рандомную строку\n' \
        '/show - показать предсказание'

        bot.send_message(chat_id, message_for_client)

    @bot.message_handler(commands=['choose_writer'])
    def choose_writer_handler(message):
        chat_id = message.chat.id

        name_writer = message.text.replace("/choose_writer@PredictionBooksBot", "")
        name_writer = name_writer.replace("/choose_writer", "")
        name_writer = name_writer.lstrip()

        try:
            clients[chat_id].writer_ = name_writer
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if not name_writer:
            bot.send_message(chat_id, myconst.need_param)
            return

        try:
            new_name = myparser.check_typos(name_writer)
            if new_name != name_writer:
                message_for_client = "Может вы имели в виду {}".format(new_name)
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="Да", callback_data=new_name),
                            telebot.types.InlineKeyboardButton(text="Нет", callback_data=name_writer))
                bot.send_message(chat_id, message_for_client, reply_markup=keyboard)
                return

            bot.send_message(chat_id, "Автор установлен")
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.callback_query_handler(func=lambda name: True)
    def inline(name):
        chat_id = name.message.chat.id
        clients[chat_id].writer_ = name.data
        bot.send_message(chat_id, "Автор установлен")

    @bot.message_handler(commands=['choose_book'])
    def choose_book_handler(message):
        chat_id = message.chat.id

        name_book = message.text.replace("/choose_book@PredictionBooksBot", "")
        name_book = name_book.replace("/choose_book", "")
        name_book = name_book.lstrip()

        name_writer = ""

        try:
            name_writer = clients[chat_id].writer_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if not name_book:
            bot.send_message(chat_id, myconst.need_param)
            return

        if not clients[chat_id].writer_:
            bot.send_message(chat_id, myconst.not_writer)
            return

        try:
            name_writer = clients[chat_id].writer_
            books = myparser.get_books(name_writer, name_book)
            clients[chat_id].books_ = books
            print(books)

            if books == {}:
                bot.send_message(chat_id, myconst.not_client_book)
                return

            message_for_client = "Какую книгу вы хотите выбрать?\n(Отправьте ее номер)\n"
            for i, book in enumerate(books.keys()):
                message_for_client += "{}) {}\n".format(i + 1, book)

            clients[chat_id].max_book_ = len(books)

            bot_msg = bot.send_message(chat_id, message_for_client)
            bot.register_next_step_handler(bot_msg, choose_book_number)
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.message_handler(commands=['get_k_random_books'])
    def get_k_random_books(message):
        chat_id = message.chat.id

        command = message.text
        command = command.replace("/get_k_random_books@PredictionBooksBot", "")
        command = command.replace("/get_k_random_books", "")

        writer = ""
        try:
            writer = clients[chat_id].writer_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if command:
            bot.send_message(chat_id, myconst.not_need_param)
            return

        if not writer:
            bot.send_message(chat_id, myconst.not_writer)
            return

        try:
            list_writers_raw = list(all_writers.keys())
            list_writers = []
            name_writer = clients[chat_id].writer_.lower()

            for name in list_writers_raw:
                list_writers.append(name.lower())

            arr_name = name_writer.split(" ")

            if name_writer.lower() not in list_writers:
                flag1 = False
                message_for_client = "Смените имя автра на возможного автора из списка\n"
                for name in list_writers:
                    print(name)
                    flag = True
                    for word in arr_name:
                        if name.find(word) == myconst.no_value:
                            flag = False
                    if flag:
                        message_for_client += "{}\n".format(name)
                        flag1 = True
                if not flag1:
                    message_for_client = "У меня нет такого автора"
                bot.send_message(chat_id, message_for_client)
                return

            books = myparser.find_all_books(name_writer, all_writers)
            max_books = len(books)
            clients[chat_id].max_book_ = max_books
            clients[chat_id].books_ = books

            message_for_client = "Выберете кол-во книг от 1 до {}".format(max_books)
            bot.msg = bot.send_message(chat_id, message_for_client)
            bot.register_next_step_handler(bot.msg, get_books)
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    def get_books(message):
        try:
            chat_id = message.chat.id
            count = message.text

            if message.content_type != "text" or not count.isdigit():
                bot.send_message(chat_id, myconst.no_understand)
                return

            count = int(count)
            if count < 1 or count > clients[chat_id].max_book_:
                message_for_client = "Номер книги вне диапозона"
                bot.send_message(chat_id, message_for_client)
                return

            name_books = list(clients[message.chat.id].books_.keys())
            new_name_books = numpy.random.choice(name_books, count, replace=False)
            new_books = {}
            for name in new_name_books:
                new_books[name] = clients[message.chat.id].books_[name]

            clients[message.chat.id].books_ = new_books
            clients[message.chat.id].max_book = count + 1

            message_for_client = "Какую книгу вы хотите выбрать?\n(Отправьте ее номер)\n"
            for i, book in enumerate(new_books.keys()):
                message_for_client += "{}) {}\n".format(i + 1, book)

            bot_msg = bot.send_message(chat_id, message_for_client)
            bot.register_next_step_handler(bot_msg, choose_book_number)
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    def choose_book_number(message):
        try:
            chat_id = message.chat.id
            number = message.text

            if message.content_type != "text" or not number.isdigit():
                bot.send_message(chat_id, myconst.no_understand)
                return

            number = int(number) - 1

            if number < 0 or number >= clients[chat_id].max_book_:
                message_for_client = "Номер книги вне диапозона"
                bot.send_message(chat_id, message_for_client)
                return

            clients[chat_id].book_ = number

            list_of_book = list(clients[chat_id].books_.values())

            max_page = myparser.max_page(list_of_book[number])
            clients[chat_id].max_page_ = max_page

            print(all_writers.keys())
            bot.send_message(chat_id, "Книга установлена")
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.message_handler(commands=['choose_page'])
    def choose_page_handler(message):
        chat_id = message.chat.id

        command = message.text
        command = command.replace("/choose_page@PredictionBooksBot", "")
        command = command.replace("/choose_page", "")

        number_book = myconst.no_value
        try:
            number_book = clients[chat_id].book_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if command:
            bot.send_message(chat_id, myconst.not_need_param)
            return

        if number_book == myconst.no_value:
            message_for_client = "Сначала выберете книгу!"
            bot.send_message(chat_id, message_for_client)
            return

        try:
            max_page = clients[chat_id].max_page_
            message_for_client = "Выберите страницу от 1 до {}".format(max_page)
            bot_msg = bot.send_message(chat_id, message_for_client)
            bot.register_next_step_handler(bot_msg, choose_page_number)
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    def choose_page_number(message):
        try:
            chat_id = message.chat.id

            number = message.text

            if message.content_type != "text" or not number.isdigit():
                message_for_client = myconst.no_understand
                bot.send_message(chat_id, message_for_client)
                return

            number = int(number) - 1

            if number < 0 or number >= clients[chat_id].max_page_:
                bot.send_message(chat_id, "Страница вне дипозона!")
                return

            clients[chat_id].page_ = number

            bot.send_message(chat_id, "Страница выбрана")
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.message_handler(commands=['get_random_page'])
    def get_random_page_handler(message):
        random.seed()

        chat_id = message.chat.id

        command = message.text
        command = command.replace("/get_random_page@PredictionBooksBot", "")
        command = command.replace("/get_random_page", "")

        number_book = myconst.no_value
        try:
            number_book = clients[chat_id].book_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if command:
            bot.send_message(chat_id, myconst.not_need_param)
            return

        if number_book == myconst.no_value:
            message_for_client = "Сначала выберете книгу!"
            bot.send_message(chat_id, message_for_client)
            return

        try:
            max_page = clients[chat_id].max_page_
            number_page = random.randint(0, max_page - 1)
            clients[chat_id].page_ = number_page

            bot.send_message(chat_id, "Выбрана {} страница".format(number_page))
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.message_handler(commands=['choose_line'])
    def choose_line_handler(message):
        chat_id = message.chat.id

        command = message.text
        command = command.replace("/choose_line@PredictionBooksBot", "")
        command = command.replace("/choose_line", "")

        number_page = myconst.no_value
        try:
            number_page = clients[chat_id].page_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if command:
            bot.send_message(chat_id, myconst.not_need_param)
            return

        if number_page == myconst.no_value:
            message_for_client = "Сначала выберете страницу!"
            bot.send_message(chat_id, message_for_client)
            return

        try:
            list_of_books = list(clients[message.chat.id].books_.values())
            url = list_of_books[clients[message.chat.id].book_]
            page = clients[message.chat.id].page_
            clients[chat_id].lines_ = myparser.get_lines(url, page)

            max_line = len(clients[chat_id].lines_)
            clients[chat_id].max_line_ = max_line

            message_for_client = "Введите строку от 1 до {}".format(max_line)
            bot_msg = bot.send_message(chat_id, message_for_client)
            bot.register_next_step_handler(bot_msg, choose_line_number)
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    def choose_line_number(message):
        try:
            chat_id = message.chat.id

            number = message.text

            if message.content_type != "text" or not number.isdigit():
                bot.send_message(chat_id, myconst.no_understand)
                return

            number = int(number) - 1

            if number < 0 or number >= clients[chat_id].max_line_:
                message_for_client = "Номер строки вне диапозона"
                bot.send_message(chat_id, message_for_client)
                return

            clients[chat_id].line_ = number
            bot.send_message(chat_id, "Строка установлена")
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.message_handler(commands=['get_random_line'])
    def get_random_line_handler(message):
        random.seed

        chat_id = message.chat.id

        command = message.text
        command = command.replace("/get_random_line@PredictionBooksBot", "")
        command = command.replace("/get_random_line", "")

        number_page = myconst.no_value
        try:
            number_page = clients[chat_id].page_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if command:
            bot.send_message(chat_id, myconst.not_need_param)
            return

        if number_page == myconst.no_value:
            message_for_client = "Сначала выберете страницу!"
            bot.send_message(chat_id, message_for_client)
            return

        try:
            list_of_books = list(clients[message.chat.id].books_.values())
            url = list_of_books[clients[message.chat.id].book_]
            page = clients[message.chat.id].page_
            clients[chat_id].lines_ = myparser.get_lines(url, page)

            max_line = len(clients[chat_id].lines_)
            number_line = random.randint(0, max_line - 1)

            clients[chat_id].line_ = number_line
            bot.send_message(chat_id, "Выбрана {} строка".format(number_line + 1))
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return

    @bot.message_handler(commands=['show'])
    def show_handler(message):
        chat_id = message.chat.id

        command = message.text
        command = command.replace("/show@PredictionBooksBot", "")
        command = command.replace("/show", "")

        number_line = myconst.no_value
        try:
            number_line = clients[chat_id].line_
        except Exception:
            bot.send_message(chat_id, myconst.not_srtart)
            return

        if command:
            bot.send_message(chat_id, myconst.not_need_param)
            return

        if clients[chat_id].line_ == myconst.no_value:
            message_for_client = "Сначала выберете строку!"
            bot.send_message(chat_id, message_for_client)
            return

        try:
            number_line = clients[chat_id].line_
            line = clients[chat_id].lines_[number_line]
            print(line)
            bot.send_message(chat_id, line)
        except Exception:
            bot.send_message(chat_id, myconst.unknow_error)
            return




    """"# Показывает всех вызможных писателей.
    @bot.message_handler(commands=['show_writers'])
    def show_writers_handler(message):

        message_for_client = "Список писателей:\n"
        for i, name in enumerate(list(all_writers.keys())):
            message_for_client += "{}) {}\n".format(i, name)

        chat_id = message.chat.id
        bot.send_message(chat_id, message_for_client)"""

    start_bot()

if __name__ == "__main__":
    chat()
