import classclient
import myparser
import telebot

#TODO: Сделать, что бы не ломался

TOKEN = '304243519:AAGRSN21G8Ft0eO5QBKlf79-q-dpSnzjrJA'
bot = telebot.TeleBot(TOKEN)

def chat():
    clients = {}

    def start_bot():

        # Заставим бота "висеть" и ждать команды.
        bot.polling(none_stop=True)

    # Обработчик команды /start.
    @bot.message_handler(commands=['start'])
    def handler_start(message):
        client = classclient.Client(message.chat.id)
        clients[message.chat.id] = client

        #Создадим клавиатуру с разными вариантами.
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True)
        keyboard.row("Выбрать автора")
        keyboard.row("Ненужная кнопка")

        bot_msg = bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)

    # Обработчик команды /stop
    @bot.message_handler(commands=['stop'])
    def handler_stop(message):
        while True:
            continue

    # Обработчик действий пользователя.
    def handler(message):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True)
        keyboard.row("Выбрать автора")
        keyboard.row("Ненужная кнопка")

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

        bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                    "Попробуйте снова!",
                                   reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)


    # Выбор автора.
    def choose_author(message):
        if (message.content_type != "text"):
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_author)
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
                keyboard.row("Ненужная Кнопка")
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
            keyboard.row("Ненужная Кнопка")
            bot_msg = bot.send_message(message.chat.id, "Что вы хотите сделать дальше?",
                                       reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, handler)

    # Выбор книги.
    def choose_book(message):
        if (message.content_type != "text"):
            bot_msg = bot.send_message(message.chat.id, "Я вас не понимаю."
                                                        "Попробуйте снова!")
            bot.register_next_step_handler(bot_msg, choose_author)
            return

        name_of_book = message.text

        clients[message.chat.id].append_books(clients[message.chat.id].writer_,
                                              name_of_book)

        if (clients[message.chat.id].books_ == {}):
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Выбрать автора")
            keyboard.row("Выбрать книгу")

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
        number_book = message.text
        clients[message.chat.id].book_ = int(number_book) - 1

        list_of_books = list(clients[message.chat.id].books_.values())
        max_number_of_page = myparser.max_page(list_of_books[int(number_book)])
        clients[message.chat.id].max_page_ = max_number_of_page

        bot_msg = bot.send_message(message.chat.id, "Выберете страницу от 1 до "
                                   + str(max_number_of_page))

        bot.register_next_step_handler(bot_msg, choose_line)

    def choose_line(message):
        tmp = message.text
        if (tmp.isdigit()):
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
        if (line.isdigit()):
            list_of_books = list(clients[message.chat.id].books_.values())
            url = list_of_books[clients[message.chat.id].book_]
            page = clients[message.chat.id].page_
            ans = myparser.get_line(url, page, int(line))
            if (ans == "*ERROR*"):
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


    start_bot()

if __name__ == "__main__":
    chat()
