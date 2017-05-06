import classclient
import myparser
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
                             "Для начала вам стоит вызвать команду \help и " \
                             "посмотреть все мои инструкции!\nХороших предсказаний!\n"
        chat_id = message.chat.id
        bot.send_message(chat_id, message_for_client)

    @bot.message_handler(commands=['help'])
    def help_handler(message):
        a = 5

    @bot.message_handler(commands=['choose_writer'])
    def choose_writer_handler(message):
        chat_id = message.chat.id

        name_writer = message.text.replace("/choose_writer ", "")

        if name_writer == "":
            bot.send_message(chat_id, "Нужен 1 параметр")
            return

        new_name = myparser.check_typos(name_writer)
        clients[chat_id].writer_ = name_writer

        if new_name != name_writer:
            message_for_client = "Может вы имели в виду {}".format(new_name)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text="Да", callback_data=new_name),
                         telebot.types.InlineKeyboardButton(text="Нет", callback_data=name_writer))
            bot.send_message(chat_id, message_for_client, reply_markup=keyboard)
            return

        bot.send_message(chat_id, "Автор установлен")


    @bot.callback_query_handler(func=lambda name: True)
    def inline(name):
        chat_id = name.message.chat.id
        clients[chat_id].writer_ = name.data
        bot.send_message(chat_id, "Автор установлен")

    @bot.message_handler(commands=['choose_book'])
    def choose_book_handler(message):
        chat_id = message.chat.id

        name_book = message.text.replace("/choose_book ", "")

        if name_book == "":
            bot.send_message(chat_id, "Нужен 1 параметр")
            return

        if clients[chat_id].writer_ == "":
            message_for_client = "Сначала выберете автора!"
            bot.send_message(chat_id, message_for_client)
            return

        name_writer = clients[chat_id].writer_
        books = myparser.get_books(name_writer, name_book)
        clients[chat_id].books_ = books
        print(books)

        if books == {}:
            message_for_client = "Такой книги нет("
            bot.send_message(chat_id, message_for_client)
            return

        message_for_client = "Какую книгу вы хотите выбрать?\n(Отправьте ее номер)\n"
        for i, book in enumerate(books.keys()):
            message_for_client += str(i + 1) + ") " + book + "\n"

        clients[chat_id].max_book_ = len(books)

        bot_msg = bot.send_message(chat_id, message_for_client)
        bot.register_next_step_handler(bot_msg, choose_book_number)

    @bot.message_handler(commands=['k_random_books'])
    def k_random_books(message):
        chat_id = message.chat.id

        if message.text.replace("/k_random_books ", "") != "":
            bot.send_message(chat_id, "Команда не принимает аргументов")
            return

        if clients[chat_id].writer_ == "":
            message_for_client = "Сначала выберете автора!"
            bot.send_message(chat_id, message_for_client)
            return

    def choose_book_number(message):
        chat_id = message.chat.id
        number = message.text

        if message.content_type != "text" or not number.isdigit():
            message_for_client = "Извините, я вас не могу понять=("
            bot.send_message(chat_id, message_for_client)
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

    @bot.message_handler(commands=['choose_page'])
    def choose_page_handler(message):
        chat_id = message.chat.id

        if message.text.replace("/choose_page", "") != "":
            bot.send_message(chat_id, "Команда не принимает аргументов")
            return

        if clients[chat_id].book_ == -1:
            message_for_client = "Сначала выберете книгу!"
            bot.send_message(chat_id, message_for_client)
            return

        max_page = clients[chat_id].max_page_
        message_for_client = "Выберите страницу от 1 до {}".format(max_page)
        bot_msg = bot.send_message(chat_id, message_for_client)
        bot.register_next_step_handler(bot_msg, choose_page_number)

    def choose_page_number(message):
        chat_id = message.chat.id

        number = message.text

        if message.content_type != "text" or not number.isdigit():
            message_for_client = "Извините, я вас не могу понять=("
            bot.send_message(chat_id, message_for_client)
            return

        number = int(number) - 1

        if number < 0 or number >= clients[chat_id].max_page_:
            bot.send_message(chat_id, "Страница вне дипозона!")
            return

        clients[chat_id].page_ = number

        bot.send_message(chat_id, "Страница выбрана")

    @bot.message_handler(commands=['get_random_page'])
    def get_random_page_handler:
        return

    @bot.message_handler(commands=['choose_line'])
    def choose_line_handler(message):
        chat_id = message.chat.id

        if message.text.replace("/choose_line", "") != "":
            bot.send_message(chat_id, "Команда не принимает аргументов")
            return

        if clients[chat_id].page_ == -1:
            message_for_client = "Сначала выберете страницу!"
            bot.send_message(chat_id, message_for_client)
            return

        list_of_books = list(clients[message.chat.id].books_.values())
        url = list_of_books[clients[message.chat.id].book_]
        page = clients[message.chat.id].page_
        clients[chat_id].lines_ = myparser.get_lines(url, page)

        max_line = len(clients[chat_id].lines_)

        message_for_client = "Введите строку от 1 до {}".format(max_line)
        bot_msg = bot.send_message(chat_id, message_for_client)
        bot.register_next_step_handler(bot_msg, choose_line_number)

    def choose_line_number(message):
        chat_id = message.chat.id

        number = message.text

        if message.content_type != "text" or not number.isdigit():
            message_for_client = "Извините, я вас не могу понять=("
            bot.send_message(chat_id, message_for_client)
            return

        number = int(number) - 1

        if number < 0 or number >= clients[chat_id].max_page_:
            message_for_client = "Номер страницы вне диапозона"
            bot.send_message(chat_id, message_for_client)
            return

        clients[chat_id].line_ = number
        bot.send_message(chat_id, "Строка установлена")

    @bot.message_handler(commands=['get_random_line'])
    def get_random_line_handler(message):
        random.seed

        chat_id = message.chat.id

        if message.text.replace("/get_random_line", "") != "":
            bot.send_message(chat_id, "Команда не принимает аргументов")
            return

        if clients[chat_id].page_ == -1:
            message_for_client = "Сначала выберете страницу!"
            bot.send_message(chat_id, message_for_client)
            return

        list_of_books = list(clients[message.chat.id].books_.values())
        url = list_of_books[clients[message.chat.id].book_]
        page = clients[message.chat.id].page_
        clients[chat_id].lines_ = myparser.get_lines(url, page)

        max_line = len(clients[chat_id].lines_)
        number_line = random.randint(0, max_line - 1)

        clients[chat_id].line_ = number_line
        bot.send_message(chat_id, "Выбрана {} строка".format(number_line + 1))


    @bot.message_handler(commands=['show'])
    def show_handler(message):
        chat_id = message.chat.id

        if message.text.replace("/show", "") != "":
            bot.send_message(chat_id, "Команда не принимает аргументов")
            return

        if clients[chat_id].line_ == -1:
            message_for_client = "Сначала выберете строку!"
            bot.send_message(chat_id, message_for_client)
            return

        number_line = clients[chat_id].line_
        line = clients[chat_id].lines_[number_line]
        bot.send_message(chat_id, line)




    # Показывает всех вызможных писателей.
    @bot.message_handler(commands=['show_writers'])
    def show_writers_handler(message):

        message_for_client = "Список писателей:\n"
        for i, name in enumerate(all_writers.keys()):
            message_for_client += "{}) {}".format(i, name)

        chat_id = message.chat.id
        bot.send_message(chat_id, message_for_client)


    """"# Обработчик команды /start.
    @bot.message_handler(commands=['start'])
    def handler_start(message):
        client = client.Client(message.chat.id)
        clients[message.chat.id] = client

        # Создадим клавиатуру с разными вариантами.
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True)
        keyboard.row("Выбрать автора")
        keyboard.row("Помощь")

        bot_msg = bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)

    # Обработчик действий пользователя.
    def handler(message):
        if clients[message.chat.id].writer_ == "":
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Выбрать автора")
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True)
            keyboard.row("Выбрать автора")
            keyboard.row("Выбрать книгу")
            keyboard.row("Получить несколько случайных книг")
            keyboard.row("Закончить")

        if (message.content_type != "text"):
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!",
                                       reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, handler)
            return

        if message.text == "Выбрать автора":
            bot_msg = bot.send_message(message.chat.id, "Введите имя и фамилию")
            bot.register_next_step_handler(bot_msg, choose_author)
            return

        if message.text == "Выбрать книгу":
            bot_msg = bot.send_message(message.chat.id, "Введите название")
            bot.register_next_step_handler(bot_msg, choose_book)
            return

        if message.text == "Получить несколько случайных книг":
            all_writers = myparser.find_all_writers()
            name_writers = clients[message.chat.id].writer_
            list_writers = []
            for name in list(all_writers.keys()):
                list_writers.append(name.lower())
            if name_writers.lower() not in list_writers:
                message_for_client = "Выберете возможного автора из списка\n"
                for name in list(all_writers.keys()):
                    if name.lower().find(name_writers.lower()) != -1:
                        message_for_client += "{}\n".format(name)
                bot_msg = bot.send_message(message.chat.id, message_for_client)
                bot.register_next_step_handler(bot_msg, choose_author2)
                return

            clients[message.chat.id].books_ = myparser.find_all_books(name_writers, all_writers)
            max_books = len(clients[message.chat.id].books_)
            bot_msg = bot.send_message(message.chat.id, "Введите кол-во книг < "
                                       + str(max_books))
            bot.register_next_step_handler(bot_msg, choose_rand_book)
            return


        bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                    "Попробуйте снова!",
                                   reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)


    # Выбор автора.
    def choose_author(message):
        if (message.content_type != "text"):
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_author2)
            return

        writer = message.text
        clients[message.chat.id].append_writer(writer)
        new_writer = myparser.check_typos(writer)

        # Если удалось исправить опечатку, то предложим пользователю изменить выбор.
        if (new_writer != writer):

            # Функция для изменения имени.
            def yes_or_no(message):
                if message.text == "Да":
                    clients[message.chat.id].append_writer(myparser.check_typos(writer))

                keyboard = telebot.types.ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    one_time_keyboard=True)
                keyboard.row("Выбрать книгу")
                keyboard.row("Получить несколько случайных книг")
                bot_msg = bot.send_message(message.chat.id,
                                           "Что вы хотите сделать дальше?",
                                           reply_markup=keyboard)
                bot.register_next_step_handler(bot_msg, handler)

            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Да", "Нет")
            bot_msg = bot.send_message(message.chat.id, "Может быть вы имели в виду: "
                                       + new_writer, reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, yes_or_no)

        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Выбрать книгу")
            keyboard.row("Получить несколько случайных книг")
            bot_msg = bot.send_message(message.chat.id, "Что вы хотите сделать дальше?",
                                       reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, handler)

    def choose_author2(message):
        if (message.content_type != "text"):
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_author2)
            return

        clients[message.chat.id].writer_ = message.text
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True)
        keyboard.row("Выбрать книгу")
        keyboard.row("Получить несколько случайных книг")
        bot_msg = bot.send_message(message.chat.id, "Что вы хотите сделать дальше?",
                                   reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)


    # Выбор книги.
    def choose_book(message):
        name_of_book = message.text
        clients[message.chat.id].append_books(clients[message.chat.id].writer_,
                                              name_of_book)

        if (message.content_type != "text"):
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Выбрать автора")
            keyboard.row("Выбрать книгу")
            keyboard.row("Получить несколько случайных книг")
            keyboard.row("Завершить")
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!",
                                       reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, handler)
            return

        if (clients[message.chat.id].books_ == {}):
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Выбрать автора")
            keyboard.row("Выбрать книгу")
            keyboard.row("Получить несколько случайных книг")

            bot_msg = bot.send_message(message.chat.id, "Такой книги нет(""
                                                        "Что вы хотите сделать?",
                                       reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, handler)
            return

        message_for_client = "Какую книгу вы хотите выбрать?\n(Отправьте ее номер)\n"

        for i,book in enumerate(clients[message.chat.id].books_.keys()):
            message_for_client += str(i + 1) + ") " +  book + "\n"

        bot_msg = bot.send_message(message.chat.id, message_for_client)
        bot.register_next_step_handler(bot_msg, choose_page)

    def choose_rand_book(message):
        if (message.content_type != "text"):
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_rand_book)
            return

        count = int(message.text)
        length = len(clients[message.chat.id].books_)

        if count <= 0 and count > length:
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_rand_book)
            return

        name_books = list(clients[message.chat.id].books_.keys())
        new_name_books = numpy.random.choice(name_books, count, replace=False)
        new_books = {}
        for name in new_name_books:
            new_books[name] = clients[message.chat.id].books_[name]

        clients[message.chat.id].books_ = new_books

        if (clients[message.chat.id].books_ == {}):
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Выбрать автора")
            keyboard.row("Выбрать книгу")
            keyboard.row("Получить несколько случайных книг")

            bot_msg = bot.send_message(message.chat.id, "Такой книги нет("
                                                        "Повторите попытку!\n"
                                                        "Что вы хотите сделать?",
                                       reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, handler)
        else:
            message_for_client = "Какую книгу вы хотите выбрать?\n(Отправьте ее номер)\n"
            for i,book in enumerate(clients[message.chat.id].books_.keys()):
                message_for_client += str(i + 1) + ") " +  book + "\n"

            bot_msg = bot.send_message(message.chat.id, message_for_client)
            bot.register_next_step_handler(bot_msg, choose_page)



    def choose_page(message):
        if (message.content_type != "text"):
            message_for_client = "Какую книгу вы хотите выбрать?\n(Отправьте ее номер)\n"
            for i, book in enumerate(clients[message.chat.id].books_.keys()):
                message_for_client += str(i + 1) + ") " + book + "\n"

            bot_msg = bot.send_message(message.chat.id, message_for_client)
            bot.register_next_step_handler(bot_msg, choose_page)
            return

        number_book = message.text
        clients[message.chat.id].book_ = int(number_book) - 1

        list_of_books = list(clients[message.chat.id].books_.values())
        max_number_of_page = myparser.max_page(list_of_books[int(number_book) - 1])
        clients[message.chat.id].max_page_ = max_number_of_page

        bot_msg = bot.send_message(message.chat.id, "Выберете страницу от 1 до "
                                   + str(max_number_of_page))

        bot.register_next_step_handler(bot_msg, choose_line)

    def choose_line(message):
        if message.content_type != "text":
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_line)
            return

        tmp = message.text
        if tmp.isdigit():
            number_page = int(tmp)
            if (number_page > 0 and number_page <= clients[message.chat.id].max_page_):
                clients[message.chat.id].page_ = number_page - 1

                bot_msg = bot.send_message(message.chat.id, "Введите номер строки")
                bot.register_next_step_handler(bot_msg, get_answer)
            else:
                bot_msg = bot.send_message(message.chat.id, "Попробуйте снова!\n"
                                                            "Введите страницу")

                bot.register_next_step_handler(bot_msg, choose_line)
        else:
            bot_msg = bot.send_message(message.chat.id, "Попробуйте снова!\n"
                                                        "Введите страницу")

            bot.register_next_step_handler(bot_msg, choose_line)

    def get_answer(message):
        line = message.text
        if line.isdigit():
            list_of_books = list(clients[message.chat.id].books_.values())
            url = list_of_books[clients[message.chat.id].book_]
            page = clients[message.chat.id].page_
            ans = myparser.get_line(url, page, int(line))
            if ans == "*ERROR*":
                bot_msg = bot.send_message(message.chat.id,
                                           "Попробуйте снова!\n"
                                           "Введите номер строки")

                bot.register_next_step_handler(bot_msg, get_answer)
            else:
                bot_msg = bot.send_message(message.chat.id, ans)

        else:
            bot_msg = bot.send_message(message.chat.id, "Попробуйте снова!\n"
                                                        "Введите номер строки")

            bot.register_next_step_handler(bot_msg, get_answer)
            """

    start_bot()

if __name__ == "__main__":
    chat()
