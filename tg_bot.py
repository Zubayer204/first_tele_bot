from telegram import *
from telegram.ext import *
import wikipedia
import requests

bot = Bot("1559095058:AAFkUrNw18iwHzYauzG4Qb4Rc_oYK6M4KhQ")

print(bot.get_me())

updater = Updater("1559095058:AAFkUrNw18iwHzYauzG4Qb4Rc_oYK6M4KhQ", use_context=True)

dispatcher: Dispatcher = updater.dispatcher

keyword = ''
chat_id = ''

def test1(update:Update,context:CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome",
        parse_mode=ParseMode.HTML
    )

def showKeyboard(update:Update, context:CallbackContext):
    global keyword, chat_id

    keyword = update.message.text
    chat_id = update.message.chat_id

    keyboard = [[
        InlineKeyboardButton("ABOUT", callback_data="ABOUT"),
        InlineKeyboardButton("IMAGE", callback_data="IMAGE")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please Choose:",reply_markup=reply_markup)


def button_click(update:Update, context:CallbackContext):
    global keyword, chat_id

    query:CallbackQuery = update.callback_query

    if query.data == "ABOUT":
        try:
            summary = wikipedia.summary(keyword)
        except wikipedia.exceptions.PageError:
            summary = "Can't find info in wikipedia"

        bot.send_message(
            chat_id=update.effective_chat.id,
            text=summary,
            parse_mode=ParseMode.HTML
        )

    if query.data == "IMAGE":

        headers = {
            "apikey": "c2962ce0-5d86-11eb-aaee-b5084cbf67d3"}

        params = (
            ("q", keyword),
            ("tbm", "isch"),
        )

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);
        data = response.json()

        first_image = data['image_results'][0]['thumbnail']

        bot.send_photo(chat_id=chat_id, photo=first_image)



dispatcher.add_handler(MessageHandler(Filters.text, showKeyboard))

dispatcher.add_handler(CallbackQueryHandler(button_click))
updater.start_polling()