#!/usr/bin/python
import telebot
from telebot import types
from edition import *
from time_com import *
from bloomberg import *
from translatepy import Translator
import random

t = '5888626392:AAH-okRsPvNVB2Zzt680b_jt2JfdyrVgLXk'
b = telebot.TeleBot(t)
translator = Translator()

while 1:
    try:
        def btn(text):
            return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(text))


        def america(msg):
            posts = edition()
            posts += time()
            posts += bloomberg()

            if len(posts) > 9:
                posts = random.sample(posts, 9)

            for i in range(len(posts)):
                if len(str(posts[i][0]) + str(posts[i][1])) <= 1000:
                    p = str(posts[i][0]) + str(posts[i][1].replace('      ', ''))
                else:
                    p = posts[i][0]

                post = translator.translate(p, 'Ukrainian')
                posts[i] = str(post) + '#$#' + str(posts[i][-1])

            with open('posts.txt', 'w') as f:
                posts = ' -#- '.join(posts)
                f.write(posts)
                f.close()

            if posts:
                markup = types.InlineKeyboardMarkup(row_width=2).add(
                    types.InlineKeyboardButton(text='Назад ⬅️', callback_data='!&-1'),
                    types.InlineKeyboardButton(text='Вперёд ➡️', callback_data='!&1'))

                img = posts.split(' -#- ')[0].split('#$#')[-1]
                post = posts.split(' -#- ')[0].split('#$#')[0]

                print(1)
                if 'http' in img:
                    b.send_photo(msg.chat.id, photo=img, caption=post, reply_markup=markup)
                else:
                    b.send_message(msg.chat.id, post, reply_markup=markup)


        def two_pattern(msg):
            # posts = tg_sending(-1001280851066)
            # posts += tg_sending(-1001443905793)
            # posts += tg_sending(-1001290660837)
            #
            # b.send_message(msg.chat.id, posts)
            pass


        def back(call):
            with open('posts.txt') as f:
                posts = f.readlines()
                posts = ''.join(posts).split(' -#- ')
                f.close()

            i = int(call.data.replace('!&', ''))
            img = posts[i].split('#$#')[-1].replace(' ', '')
            post = posts[i].split('#$#')[0]
            markup = types.InlineKeyboardMarkup(row_width=2)
            print(i, post)
            if 0 <= i <= len(posts)-1:
                markup.add(
                    types.InlineKeyboardButton(text='Назад ⬅️', callback_data='!&' + str(i - 1)),
                    types.InlineKeyboardButton(text='Вперед ➡️', callback_data='!&' + str(i + 1)))

                b.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                if 'http' in img:
                    b.send_photo(call.message.chat.id, photo=img, caption=post, reply_markup=markup)
                else:
                    b.send_message(call.message.chat.id, post, reply_markup=markup)

        @b.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.data == 'Америка 🇺🇸':
                b.send_message(call.message.chat.id, 'Загрузка постов...')
                america(call.message)

            if call.data == '2 шаблон':
                pass

            if '!&' in call.data:
                back(call)


        @b.message_handler()
        def get_user_text(msg):
            txt = msg.text

            if txt == '/start':
                b.send_message(msg.chat.id, 'Главное меню', reply_markup=btn('Получить информацию 📩'))

            if txt == 'Получить информацию 📩':
                markup = types.InlineKeyboardMarkup(row_width=2).add(
                    types.InlineKeyboardButton(text='Америка 🇺🇸', callback_data='Америка 🇺🇸'),
                    types.InlineKeyboardButton(text='2 шаблон', callback_data='2 шаблон'))
                b.send_message(msg.chat.id, 'Выберите шаблон', reply_markup=markup)


        b.polling(none_stop=True)

    except Exception as ex:
        print(ex)
