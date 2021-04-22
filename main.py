import requests
import json
import sqlite3
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


markup = None


def main():
    updater = Updater('1736375279:AAG2gSCg8SbMsHgF7GkgRKkMT8DfOnJNo2g', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_))
    dp.add_handler(CommandHandler('Russian', ru))
    dp.add_handler(CommandHandler('English', en))
    dp.add_handler(CommandHandler('German', de))
    dp.add_handler(CommandHandler('French', fr))
    dp.add_handler(CommandHandler('Italian', it))
    dp.add_handler(CommandHandler('Japanese', ja))

    text_handler = MessageHandler(Filters.text, translate)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


def start(update, context):
    global markup
    # Проверка, есть ли уже пользователь в базе данных, если нет,
    # то добавить его туда, чтобы потом можно было изменять язык
    # конкретно для данного пользователя
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'SELECT * FROM users WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    result = cur.fetchall()
    if result is None or result == []:
        s = 'INSERT INTO users (user_id) VALUES ({})'.format(user_id)
        cur.execute(s)
        s = 'INSERT INTO users (lang) VALUES ("ru")'
        cur.execute(s)
        con.commit()

        reply_keyboard = [['/Russian', '/English', '/German'],
                          ['/French', '/Italian', '/Japanese']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Hello, firstly, choose language to translate'
            '\n'
            'Help -> /help',
            reply_markup=markup)
    else:
        reply_keyboard = [['/Russian', '/English', '/German'],
                          ['/French', '/Italian', '/Japanese']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Hello again',
            reply_markup=markup
        )


def help_(update, context):
    update.message.reply_text(
        'Open the keyboard to choose language')


def ru(update, context):
    global markup
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'UPDATE users SET lang = "ru" WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    con.commit()

    update.message.reply_text('Russian is selected')
    update.message.reply_text('Russian is selected', reply_markup=ReplyKeyboardRemove)


def en(update, context):
    global markup
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'UPDATE users SET lang = "en" WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    con.commit()

    update.message.reply_text('English is selected')
    update.message.reply_text('English is selected', reply_markup=ReplyKeyboardRemove)


def de(update, context):
    global markup
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'UPDATE users SET lang = "de" WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    con.commit()

    update.message.reply_text('German is selected')
    update.message.reply_text('German is selected', reply_markup=ReplyKeyboardRemove)


def fr(update, context):
    global markup
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'UPDATE users SET lang = "fr" WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    con.commit()

    update.message.reply_text('French is selected')
    update.message.reply_text('French is selected', reply_markup=ReplyKeyboardRemove)


def it(update, context):
    global markup
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'UPDATE users SET lang = "it" WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    con.commit()

    update.message.reply_text('Italian is selected')
    update.message.reply_text('Italian is selected', reply_markup=ReplyKeyboardRemove)


def ja(update, context):
    global markup
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'UPDATE users SET lang = "ja" WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    con.commit()

    update.message.reply_text('Japanese is selected')
    update.message.reply_text('Japanese is selected', reply_markup=ReplyKeyboardRemove)


def translate(update, context):
    con = sqlite3.connect('userdata.sqlite')
    cur = con.cursor()
    user_id = str(update.message.from_user.id)
    s = 'SELECT * FROM users WHERE user_id = {}'.format(user_id)
    cur.execute(s)
    result = cur.fetchall()

    text = update.message.text.split('\n')
    message = translate_(text, result[0][1])
    update.message.reply_text(message)


def translate_(text, lang):
    token = 't1.9euelZrMk8rJkZmTnJyYxs6aipDMne3rnpWay5aVnsfNmJ6Oxs_MzMiUlI7l8_dAVnt7-e9_DiQo_N3z9wAFeXv5738OJCj8.' \
            'AtSIM2vXIjOKHHCdlVDa1B4IlJogRQX66ImUCzcmupZ6gd_nAMeqyhEdqamL8Lu9v4mCZmh0o8mVXd4HiimODQ'

    headers = {'Authorization': 'Bearer ' + token}

    body = {
        'folder_id': 'b1g4n8j8mafa910al4ai',
        'texts': text,
        'targetLanguageCode': lang
    }

    json_body = json.dumps(body, ensure_ascii=False).encode('utf8')
    url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    response = requests.post(url, json_body, headers=headers)
    json_response = response.json()
    answer = ''
    for i in range(len(json_response['translations'])):
        answer += json_response['translations'][i]['text']
        answer += '\n'
    return answer


if __name__ == '__main__':
    main()
