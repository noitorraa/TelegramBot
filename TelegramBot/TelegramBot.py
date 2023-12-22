# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import wikipedia
 
print('************Запустилось************')
# Функция-обработчик команды /start
def start(update: Update, context) -> None:
    # Отправляем сообщение и цепляем клавиатуру
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Выберите язык с помощью кнопок и введите слово или словосочетание для поиска статьи на Википедии.", reply_markup=create_keyboard())

def create_keyboard():
    keyboard = [[KeyboardButton('Русский'), KeyboardButton('English')]] # Добавляем кнопки
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Функция-обработчик текстовых сообщений
def echo(update: Update, context) -> None:
    word = update.message.text
    # Изменяем язык
    if word == 'Русский':
        wikipedia.set_lang('ru')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Язык установлен на русский.')
    elif word == 'English':
        wikipedia.set_lang('en')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Language set to English.')
    else: # Таким образом запрос 'Русский' и 'English' не получится отправить для поиска инфы, но что поделать, так надо
        try:
            summary = wikipedia.summary(word) # Ищем совпадения на Википедии
            context.bot.send_message(chat_id=update.effective_chat.id, text=summary)
        except wikipedia.exceptions.DisambiguationError as e:# Если несколько экземпляров найдено
            options = "\n".join(e.options)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Пожалуйста, уточните ваш запрос:\n{options}')
        except wikipedia.exceptions.PageError:# Если ничего не найдено
            context.bot.send_message(chat_id=update.effective_chat.id, text='Статья на Википедии не найдена.')

# Функция main
def main() -> None:
    # Запускаем бота, апдэйтер работает только в старой версии какой-то
    updater = Updater(token='6778680428:AAHVe_MHKsNktGXgTReoGH4VL3KYqGDuB2Y', use_context=True)
    dispatcher = updater.dispatcher
    # Создание обработчиков команд и текстовых сообщений
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.Filters.text & (~filters.Filters.command), echo)
    # Регистрация обработчиков в диспетчере
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    # Запуск бота
    updater.start_polling()
    updater.idle()
    

# Если запущена напрямую, то будет работать
if __name__ == '__main__':
    main()
