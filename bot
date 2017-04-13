import telebot
import myparser

TOKEN = '304243519:AAGRSN21G8Ft0eO5QBKlf79-q-dpSnzjrJA'
bot = telebot.TeleBot(TOKEN)

def start_bot():

    ## Заставим бота "висеть" и ждать команды.
    bot.polling(none_stop=True)

# Обработчик команды /start.
@bot.message_handler(commands=['start'])
def handler_start(message):

    #Создадим клавиатуру с разными вариантами.
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                one_time_keyboard=True)
    keyboard.row("Выбрать Автора")
    keyboard.row("Ненужная кнопка")

    bot_msg = bot.send_message(message.chat.id, "Привет, что ты хочещь сделать?",
                     reply_markup=keyboard)
    bot.register_next_step_handler(bot_msg, handler)

## Обработчик действий пользователя.
def handler(message):
    if message.text == "Выбрать Автора":
        bot_msg = bot.send_message(message.chat.id, "Введите имя и фамилию")
        bot.register_next_step_handler(bot_msg, choose_author)

def choose_author(message):
    name = message.text
    new_name

    #Если удалось исправить опечатку, то предложим пользователю изменить выбор.
    if (new_name != ""):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True)
        keyboard.row(["Да", "Нет"])

        bot.msg = bot.send_message(message.chat.id, "Может быть вы имели в виду"
                                   + new_name, reply_markup=keyboard)

if __name__ == "__main__":
    start_bot()
