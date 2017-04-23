import classclient
import myparser
import telebot

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
        keyboard.row("Выбрать aвтора")
        keyboard.row("Ненужная кнопка")

        bot_msg = bot.send_message(message.chat.id, "Привет, что вы хотите сделать?", reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)

    # Обработчик действий пользователя.
    def handler(message):
        if message.text == "Выбрать aвтора":
            bot_msg = bot.send_message(message.chat.id, "Введите имя и фамилию")
            bot.register_next_step_handler(bot_msg, choose_author)

        if message.text == "Выбрать книгу":
            bot_msg = bot.send_message(message.chat.id, "Введите название")
            bot.register_next_step_handler(bot_msg, choose_book)

    # Выбор автора.
    def choose_author(message):
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
        name_of_book = message.text

        clients[message.chat.id].append_books(clients[message.chat.id].writer_,
                                              name_of_book)

        print(clients[message.chat.id].books_)
        message_for_client = "Какую книгу вы хотите выбрать?\n"
        for i,book in enumerate(clients[message.chat.id].books_.keys()):
            message_for_client += str(i) + ") " +  book + "\n"

        print(message_for_client)

        bot_msg = bot.send_message(message.chat.id, message_for_client, reply_markup=None)


    start_bot()

if __name__ == "__main__":
    chat()
