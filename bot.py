import telebot
import myparser

TOKEN = '304243519:AAGRSN21G8Ft0eO5QBKlf79-q-dpSnzjrJA'
bot = telebot.TeleBot(TOKEN)

def chat():
    writers = {}

    def start_bot():

        # Заставим бота "висеть" и ждать команды.
        bot.polling(none_stop=True)

    # Обработчик команды /start.
    @bot.message_handler(commands=['start'])
    def handler_start(message):
        #Создадим клавиатуру с разными вариантами.
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                    one_time_keyboard=True)
        keyboard.row("Выбрать aвтора")
        keyboard.row("Ненужная кнопка")

        bot_msg = bot.send_message(message.chat.id, "Привет, что ты хочещь сделать?", reply_markup=keyboard)
        bot.register_next_step_handler(bot_msg, handler)

    # Обработчик действий пользователя.
    def handler(message):
        if message.text == "Выбрать aвтора":
            bot_msg = bot.send_message(message.chat.id, "Введите имя и фамилию")
            bot.register_next_step_handler(bot_msg, choose_author)

        if message.text == "Выбрать книгу":
            bot_msg = bot.send_message(message.chat.id, "Введите название")
            bot.register_next_step_handler(bot_msg, choose_book)

    def choose_author(message):
        writer = message.text
        writers[message.chat.id] = writer
        new_writer = myparser.check_typos(writer)

        # Если удалось исправить опечатку, то предложим пользователю изменить выбор.
        if (new_writer != writer):

            # Функция для изменения имени.
            def yes_or_no(message):
                if message.text == "Да":
                    writers[message.chat.id] = myparser.check_typos(writers[message.chat.id])




            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                         one_time_keyboard=True)
            keyboard.row("Да", "Нет")
            bot_msg = bot.send_message(message.chat.id, "Может быть вы имели в виду: "
                                       + new_writer, reply_markup=keyboard)
            bot.register_next_step_handler(bot_msg, yes_or_no)

    def choose_book(message):




    start_bot()

if __name__ == "__main__":
    chat()
