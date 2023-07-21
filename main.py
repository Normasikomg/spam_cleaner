import logging
import time
import sss

from telegram.ext import Updater, MessageHandler, Filters

token = "5325240818:AAGX_rGo-_FMaQYPedJFWYo1R2rRONkuCvg"
chat_id = '-1001978313765'

# Задаем уровень логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Проверяем сообщения на наличие запрещенных слов (можно прямо в коде добавлять список слов, либо можно создать файлик)
def bad_words(text):
    banned_words = sss.bad

    for word in banned_words:
        if word.lower() in text.lower():
            return True
    return False


# Тут обрабатываем список входящих сообщений
def echo(update, context):
    message = update.effective_message
    text = message.text
    user = message.from_user
    username = user.username

    # Удалим сообщение, но только через 3 минуты (вариативно), чтобы все чуханы посмотрели
    # Можно добавить функцию, чтобы за плохие слова банило участника, типа Колю)
    if bad_words(text):
        time.sleep(3)
        message.delete()
        if username is not None:
            context.bot.send_message(chat_id=chat_id,
                                     text=f"@{username},⚠️ Вы использовали запрещенные слова. Пожалуйста,"
                                          " не повторяйте это.")
        else:
            context.bot.send_message(chat_id=chat_id,
                                     text=f"Пользователь без ника,⚠️ Вы использовали запрещенные слова. Пожалуйста,"
                                          " не повторяйте это.")
    else:
        print(text)


def main():
    bot_token = token
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    # Запускаем бота (бесконечно)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
