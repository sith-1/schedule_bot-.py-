import logging
import requests
from docx import Document
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция для загрузки расписания
def download_schedule(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('schedule.docx', 'wb') as f:
            f.write(response.content)
        return 'schedule.docx'
    else:
        return None


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте команду /schedule для получения расписания.')


# Функция для обработки команды /schedule
def schedule(update: Update, context: CallbackContext) -> None:
    url = 'URL_ВАШЕГО_РАСПИСАНИЯ'  # Замените на URL вашего расписания
    filename = download_schedule(url)

    if filename:
        doc = Document(filename)
        schedule_text = ""

        for para in doc.paragraphs:
            schedule_text += para.text + "\n"

        update.message.reply_text(schedule_text[:4000])  # Ограничиваем размер сообщения
    else:
        update.message.reply_text('Не удалось загрузить расписание.')


def main() -> None:
    # Вставьте ваш токен здесь
    updater = Updater("2080903790:AAGMBTeJ_5fdYkN9j-sdJ9wO-iQeSff-ZOY")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("schedule", schedule))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
