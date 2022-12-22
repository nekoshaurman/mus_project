import pandas as pd
import numpy as np
import transform_data as data
import telebot
import authorization
from telebot import types
import random

bot = telebot.TeleBot(authorization.bot_token())

dataset_music = data.get_dataset("data_copy3.csv")
dataset_users = data.get_users("data_users.csv")
user_id = 0
list_to_user = pd.DataFrame()
track_n = 0


@bot.message_handler(commands=['start'])
def start(message):
    rnd = random.randint(1, 2)
    if rnd == 1:
        bot.send_video(message.chat.id, 'https://media.tenor.com/LYUe1FNHN-UAAAAC/cat-headphones.gif')
    if rnd == 2:
        bot.send_video(message.chat.id, 'https://media.tenor.com/82Rr2PPBCtIAAAAd/cat-jam-cat.gif')
    mess = f'Привет <b>{message.from_user.first_name}</b> 👋.\n\n<b>NekkoMusic</b> 🎧 - музыкальный бот, ' \
           f'который всегда с ' \
           f'тобой на <u>одной волне 🎵</u>.\n\n💿 Мы поможем подобрать тебе плейлист мечты! 💿\n\nНапиши /menu, ' \
           f'чтобы насладится ' \
           f'прекрасными музыкальными композциями.\n '
    global user_id
    user_id = message.from_user.id
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    start = types.KeyboardButton('👋 Рекомендации')
    like_playlist = types.KeyboardButton('🎼 Плейлист лайков ❤')
    help_menu = types.KeyboardButton('❓ Помощь')

    markup.add(start, like_playlist, help_menu)
    bot.send_message(message.chat.id,
                     f'Перед тобой интерактивное меню, нажми:\n\n'
                     f'👋<b> Рекомендации</b> - чтобы бот подобрал для тебя плейлист,\n\n'
                     f'🎼<b> Плейлист лайков</b> ❤ - чтобы бот подобрал для тебя,\n\n'
                     f'❓<b> Помощь</b> - узнать все команды.\n\n',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(
    content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location",
                   "contact",
                   "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                   "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                   "migrate_from_chat_id", "pinned_message"])
def get_mode(message):
    if message.text == "👋 Рекомендации":
        global user_id
        global list_to_user
        if user_id in dataset_users["id"].unique():
            user_favorite = []
            favorite = dataset_users.loc[dataset_users.id == user_id]
            user_favorite.append(favorite.iloc[0]["likelist"])
        else:
            user_favorite = []

        list_to_user = data.get_list(dataset_music, user_favorite)

        like_dislike(message)

    elif message.text == "🎼 Плейлист лайков ❤":
        liked_playlist(message)

    elif message.text == "❓ Помощь":
        help_menu(message)

    else:
        bot.send_message(message.from_user.id, text="Я тебя не понимаю 🤔")
        menu(message)


def help_menu(message):
    bot.send_message(message.chat.id,
                     f'❤ - Лайкнуть трек, чтобы чаще его слышать\n'
                     f'💔 - Уменьшить шанс появления данной композиции\n'
                     f'🚪 - Вернуться в меню\n'
                     f'🎼 - Просмотреть список лайкнутых треков\n',
                     parse_mode='html')


def liked_playlist(message):
    global user_id
    tracks = ""
    if user_id in dataset_users["id"].unique():
        user_favorite = dataset_users.loc[dataset_users.id == user_id]
        user_favorite = user_favorite.iloc[0]["likelist"]
        count_likes = len(user_favorite)
    else:
        user_favorite = []
        count_likes = 0

    if count_likes > 0:
        count = 0
        for track in range(0, count_likes):
            track_id = user_favorite[track]
            track_name = dataset_music.loc[dataset_music.id == track_id]
            artist_name = track_name.iloc[0]["artist_name"]
            track_name = track_name.iloc[0]["track_name"]
            track_text = str(track + 1) + ". " + track_name + " --- " + artist_name + "\n"
            tracks += track_text
            count += 1
            if count == 30 or track == count_likes - 1:
                count = 0
                bot.send_message(message.chat.id,
                                 text=tracks,
                                 parse_mode='html')
                tracks = ""
    else:
        bot.send_message(message.chat.id,
                         text="Кажется вы еще ничего не лайкнули :c",
                         parse_mode='html')


def like_dislike(message):
    global track_n
    global list_to_user
    kb = types.InlineKeyboardMarkup(row_width=3)
    btn0 = types.InlineKeyboardButton(text='❤', callback_data='❤')
    btn1 = types.InlineKeyboardButton(text='💔', callback_data='💔')
    btn2 = types.InlineKeyboardButton(text='🚪', callback_data='🚪')
    kb.add(btn0, btn1, btn2)

    track_to_user = list_to_user.iloc[track_n]
    artist_name = track_to_user.artist_name
    track_name = track_to_user.track_name
    track_text = track_name + " --- " + artist_name + "\n"
    track_n += 1

    if track_n == 20:
        track_n = 0
        bot.send_message(message.chat.id,
                         text="Вы просмотрели все предложенные треки!",
                         parse_mode='html')
        get_mode(message)

    bot.send_message(message.chat.id,
                     text=track_text,
                     reply_markup=kb)


def save_liked():
    global dataset_users
    global track_n
    global user_id

    liked_track = list_to_user.iloc[track_n-1]
    id_track = liked_track.id
    count = len(dataset_users.index)
    if count == 0:
        print("add first")
        new = np.array([id_track])
        new_user = pd.DataFrame({"id": [user_id],
                                 "likelist": [new]})
        dataset_users = pd.concat([dataset_users, new_user], ignore_index=True)
    else:
        if user_id in (dataset_users["id"].to_numpy()):
            print("add prev")
            index = dataset_users[dataset_users["id"] == user_id].index[0]
            new_list = dataset_users.loc[dataset_users.id == user_id]
            new_list = new_list.iloc[0]["likelist"]
            if id_track not in new_list:
                new_list = np.append(new_list, id_track)
            dataset_users.at[index, "likelist"] = new_list
        else:
            print("add new")
            new = np.array([id_track])
            new_user = pd.DataFrame({"id": [user_id],
                                     "likelist": [new]})
            dataset_users = pd.concat([dataset_users, new_user], ignore_index=True)

    dataset_users.to_csv("data_users.csv", sep=";", index=False)


def liked_playlist(message):
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
