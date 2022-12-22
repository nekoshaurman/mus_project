import pandas as pd
import numpy as np
import transform_data as data
import telebot
import authorization
from telebot import types


track_n = {}
list_to_user = {}

# dataset_music = data.get_dataset("data_copy3.csv")
# dataset_users = data.get_users("data_users.csv")


bot = telebot.TeleBot(authorization.bot_token())


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет <b>{message.from_user.first_name}</b> 👋.\n\n<b>NekkoMusic</b> 🎧 - музыкальный бот, ' \
           f'который всегда с ' \
           f'тобой на <u>одной волне 🎵</u>.\n\n💿 Мы поможем подобрать тебе плейлист мечты! 💿\n\nНапиши /menu, ' \
           f'чтобы насладится ' \
           f'прекрасными музыкальными композциями.\n '
    track_n[message.from_user.id] = 0
    bot.send_message(message.from_user.id, mess, parse_mode='html')


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    recommendations = types.KeyboardButton('👋 Рекомендации')
    like_playlist = types.KeyboardButton('🎼 Плейлист лайков ❤')
    help_call = types.KeyboardButton('❓ Помощь')

    markup.add(recommendations, like_playlist, help_call)
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
def get_mode(message):
    dataset_music = data.get_dataset("data_copy3.csv")
    dataset_users = data.get_users("data_users.csv")

    if message.text == "👋 Рекомендации":
        if message.from_user.id in (dataset_users["id"].to_numpy()):
            favorite = dataset_users.loc[dataset_users.id == message.from_user.id]
            user_favorite = favorite.iloc[0]["likelist"]
        else:
            user_favorite = []

        list_to_user[message.from_user.id] = data.get_list(dataset_music, user_favorite)

        like_dislike(message)

    elif message.text == "🎼 Плейлист лайков ❤":
        liked_playlist(message)

    elif message.text == "❓ Помощь":
        help_menu(message)

    else:
        bot.send_message(message.from_user.id, text="Я тебя не понимаю 🤔")
        menu(message)


def like_dislike(message):
    kb = types.InlineKeyboardMarkup(row_width=3)
    btn0 = types.InlineKeyboardButton(text='❤', callback_data='❤')
    btn1 = types.InlineKeyboardButton(text='💔', callback_data='💔')
    btn2 = types.InlineKeyboardButton(text='🚪', callback_data='🚪')
    kb.add(btn0, btn1, btn2)

    track_to_user = list_to_user[message.from_user.id].iloc[track_n[message.from_user.id]]
    artist_name = track_to_user.artist_name
    track_name = track_to_user.track_name
    track_text = track_name + " --- " + artist_name + "\n"
    track_n[message.from_user.id] += 1

    if track_n[message.from_user.id] == 20:
        track_n[message.from_user.id] = 0
        bot.send_message(message.from_user.id,
                         text="Вы просмотрели все предложенные треки!",
                         parse_mode='html')
        get_mode(message)

    bot.send_message(message.from_user.id,
                     text=track_text,
                     reply_markup=kb)


def liked_playlist(message):
    dataset_music = data.get_dataset("data_copy3.csv")
    dataset_users = data.get_users("data_users.csv")
    tracks = ""
    if message.from_user.id in dataset_users["id"].unique():
        user_favorite = dataset_users.loc[dataset_users.id == message.from_user.id]
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


def help_menu(message):
    bot.send_message(message.from_user.id,
                     f'❤ - Лайкнуть трек, чтобы чаще его слышать\n'
                     f'💔 - Уменьшить шанс появления данной композиции\n'
                     f'🚪 - Вернуться в меню\n'
                     f'🎼 - Просмотреть список лайкнутых треков\n',
                     parse_mode='html')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == '❤':
        print(list_to_user[callback.message.from_user.id])
        save_liked(callback.message)
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


def save_liked(message):
    dataset_users = data.get_users("data_users.csv")

    liked_track = list_to_user[message.from_user.id].iloc[track_n[message.from_user.id] - 1]
    id_track = liked_track.id
    count = len(dataset_users.index)  # count of users likes

    if count == 0:
        print("add first")
        new = np.array([id_track])
        new_user = pd.DataFrame({"id": [message.from_user.id],
                                 "likelist": [new]})
        dataset_users = pd.concat([dataset_users, new_user], ignore_index=True)

    elif message.from_user.id in (dataset_users["id"].to_numpy()):
        print("add prev")
        index = dataset_users[dataset_users["id"] == message.from_user.id].index[0]
        new_list = dataset_users.loc[dataset_users.id == message.from_user.id]
        new_list = new_list.iloc[0]["likelist"]
        if id_track not in new_list:
            new_list = np.append(new_list, id_track)
        dataset_users.at[index, "likelist"] = new_list

    else:
        print("add new")
        new = np.array([id_track])
        new_user = pd.DataFrame({"id": [message.from_user.id],
                                 "likelist": [new]})
        dataset_users = pd.concat([dataset_users, new_user], ignore_index=True)

    dataset_users.to_csv("data_users.csv", sep=";", index=False)


bot.polling(none_stop=True, interval=0)