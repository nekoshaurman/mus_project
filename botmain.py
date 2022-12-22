import telebot
import authorization
from telebot import types

bot = telebot.TeleBot(authorization.bot_token())


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет <b>{message.from_user.first_name}</b> 👋.\n\n<b>NekkoMusic</b> 🎧 - музыкальный бот, ' \
           f'который всегда с ' \
           f'тобой на <u>одной волне 🎵</u>.\n\n💿 Мы поможем подобрать тебе плейлист мечты! 💿\n\nНапиши /menu, ' \
           f'чтобы насладится ' \
           f'прекрасными музыкальными композциями.\n '
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    start = types.KeyboardButton('👋 Рекомендации')
    like_playlist = types.KeyboardButton('🎼 Плейлист лайков ❤')
    help = types.KeyboardButton('❓ Помощь')

    markup.add(start, like_playlist, help)
    bot.send_message(message.chat.id,
                     f'Перед тобой интерактивное меню, нажми:\n'
                     f'👋<b> Рекомендации</b> - чтобы бот подобрал для тебя плейлист,\n'
                     f'🎼<b> Плейлист лайков</b> ❤ - чтобы бот подобрал для тебя,\n'
                     f'❓<b> Помощь</b> - узнать все команды.\n',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(
    content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location",
                   "contact",
                   "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                   "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                   "migrate_from_chat_id", "pinned_message"])

def liked_playlist(message):
    print('1')

def get_mode(message):
    if message.text == "👋 Рекомендации":
        like_dislike(message)
    elif message.text == "🎼 Плейлист лайков ❤":
        liked_playlist(message)
    elif message.text == "❓ Помощь":
        help(message)
    else:
        bot.send_message(message.from_user.id, text="Я тебя не понимаю 🤔")
        menu(message)


def help(message):
    bot.send_message(message.chat.id,
                     f'❤ - Лайкнуть трек, чтобы чаще его слышать\n'
                     f'💔 - Уменьшить шанс появления данной композиции\n'
                     f'🚪 - Вернуться в меню\n'
                     f'🎼 - Просмотреть список лайкнутых треков\n',
                     parse_mode='html')


def like_dislike(message):
    kb = types.InlineKeyboardMarkup(row_width=3)
    btn0 = types.InlineKeyboardButton(text='❤', callback_data='❤')
    btn1 = types.InlineKeyboardButton(text='💔', callback_data='💔')
    btn2 = types.InlineKeyboardButton(text='🚪', callback_data='🚪')
    kb.add(btn0, btn1, btn2)

    bot.send_message(message.chat.id, 'Audio', reply_markup=kb)


def save_liked():
    print('1')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == '❤':
        save_liked()
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, text="Этот трек будет чаще в ваших наушниках! ❤")
        like_dislike(callback.message)
    elif callback.data == '💔':
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id, text="Нам тоже не очень нравится эта "
                                                                           "композиция! 🤢")
        like_dislike(callback.message)
    elif callback.data == '🚪':
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.message_id,
                              text="Мы снова в меню 🖥️")
        menu(callback.message)


bot.polling(none_stop=True, interval=0)
