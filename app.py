import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)

from bitcoin.btc import btc_scraping
from config.credentials import BOT_TOKEN, PORT, URL, ADDRESS, BOT

global BOT
global TOKEN
global ADDRESS
global PORT
TOKEN = BOT_TOKEN
BOT = BOT
PORT = PORT
ADDRESS = ADDRESS

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Edad', 'Color Favorito'],
    ['Precio del BitCoin'],
    ['Terminar'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = []

    for key, value in user_data.items():
        facts.append(f'{key} - {value}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    reply_text = "¡Hola! Mi nombre es Flipo."
    if context.user_data:
        reply_text += (
            f" Ya me has dicho esto de tí: {', '.join(context.user_data.keys())}. ¿Por qué no me cuentas algo más sobre ti? "
            f" O cambiar cualquier cosa que ya sepa :)"
        )
    else:
        reply_text += (
            " Mantendré una conversación contigo. ¿Por qué no me cuentas algo sobre ti? "
        )
    update.message.reply_text(reply_text, reply_markup=markup)

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower()
    context.user_data['choice'] = text
    if context.user_data.get(text):
        reply_text = (
            f'¿Tu {text}? ¡Ya sé sobre eso! Tienes: {context.user_data[text]}'
        )

    else:
        if text == 'precio del bitcoin':
            reply_text = (
                f'El precio de Bitcoin es de {btc_scraping()}'
            )
        else:
            reply_text = f'¿Tu {text}? ¡Sí, me encantaría saberlo!'

    update.message.reply_text(reply_text)
    return TYPING_REPLY


def custom_choice(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'De acuerdo, primero envía la categoría, por ejemplo, "Habilidad más impresionante'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    category = context.user_data['choice']
    context.user_data[category] = text.lower()
    del context.user_data['choice']

    update.message.reply_text(
        "¡Excelente! Para que lo sepas, esto es lo que ya me has dicho:"
        f" {facts_to_str(context.user_data)}"
        "Puedes contarme más o cambiar tu opinión sobre algo.",
        reply_markup=markup,
    )

    return CHOOSING


def show_data(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"Esto es lo que ya me has dicho: {facts_to_str(context.user_data)}"
    )


def done(update: Update, context: CallbackContext) -> int:
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text(
        "Aprendí esto sobre ti:" f"{facts_to_str(context.user_data)} ¡Hasta la proxima! Espero verte pronto",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='conversationbot')
    updater = Updater(token=TOKEN, persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    # Filters.regex('^(Edad|Color Favorito|Number of siblings)$'), regular_choice
                    Filters.regex('^(Edad|Color Favorito|Precio del BitCoin)$'), regular_choice,
                ),
                MessageHandler(Filters.regex('^¿Algo más?..$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Terminar')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Terminar')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Terminar'), done)],
        name="mi_conversacion",
        persistent=True,
    )

    dispatcher.add_handler(conv_handler)

    show_data_handler = CommandHandler('show_data', show_data)
    dispatcher.add_handler(show_data_handler)

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen=ADDRESS, port=PORT, url_path=TOKEN, webhook_url=URL + TOKEN)
    # updater.start_webhook(url_path=TOKEN, webhook_url=URL + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
