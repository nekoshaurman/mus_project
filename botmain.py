import telebot
import authorization
from telebot import types

bot = telebot.TeleBot(authorization.bot_token())


def get_like(message):
    global like

    #bot.send_message(message.from_user.id, "Какой трек добавить? (номер из списка)")
    try:
        like = int(message.text)
        if 1 <= like <= 10:
            bot.send_message(message.from_user.id, text="Добавлено!")
        else:
            bot.send_message(message.from_user.id, 'Что-то не так :c')
            bot.register_next_step_handler(message, get_like)
    except Exception:
        bot.send_message(message.from_user.id, 'Что-то не так :c')
        bot.register_next_step_handler(message, get_like)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    work = 2
    if message.text == "/start":
        # bot.send_message(message.from_user.id, "Привет, вот что я умею:"
        # "\n /list - получить свой персональный список треков"
        # "\n /like - добавить трек из последнего списка в избранное")

        keyboard = types.ReplyKeyboardMarkup(row_width=2)  # наша клавиатура
        key_list = types.KeyboardButton(text='/list')  # кнопка «Да»
        keyboard.add(key_list)  # добавляем кнопку в клавиатуру
        key_like = types.KeyboardButton(text='/like')
        keyboard.add(key_like)
        bot.send_message(message.from_user.id,
                         text="Привет, вот что я умею:"
                              "\n /list - получить свой персональный список треков"
                              "\n /like - добавить трек из последнего списка в избранное",
                         reply_markup=keyboard)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Вот что я умею:"
                                               "\n /list - получить свой персональный список треков"
                                               "\n /like - добавить трек из последнего списка в избранное")
    elif message.text == "/list":
        if work == 1:
            bot.send_message(message.from_user.id, "Вот твои треки:\n"
                                                   "1. Combat Heaven - Shall Burn\n"
                                                   "2. Til Tomorrow - Walker McGuire\n"
                                                   "3. The Senior - BILL STAX\n"
                                                   "4. Break Free - Ariana Grande\n"
                                                   "5. Scripture - 6LACK\n"
                                                   "6. Stonehenge - Eddie Izzard\n"
                                                   "7. Born To Be My Baby - Bon Jovi\n"
                                                   "8. Architects - Rise Against\n"
                                                   "9. This Place - Descendents\n"
                                                   "10. Fade Away - We Came As Romans\n")
            work += 1
        else:
            bot.send_message(message.from_user.id, "Вот твои треки:\n"
                                               "Вот твои треки:\n" 
                                               "1. Disconnect - Plastikman\n"
                                               "2. La bastille - Jacques Brel\n"
                                               "3. Iron Man - Black Sabbath\n"
                                               "4. Rich As Fuck - Lil Wayne\n"
                                               "5. milkyway drive - DE DE MOUSE\n"
                                               "6. Forever - Pope\n"
                                               "7. Awful - Hole\n"
                                               "8. Mary Jane - Rick James\n"
                                               "9. GOTTI - 6ix9ine\n"
                                               "10. Controlla - Drake\n")
    elif message.text == "/like":
        bot.send_message(message.from_user.id, "Какой трек добавить? (номер из списка)")
        bot.register_next_step_handler(message, get_like)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
