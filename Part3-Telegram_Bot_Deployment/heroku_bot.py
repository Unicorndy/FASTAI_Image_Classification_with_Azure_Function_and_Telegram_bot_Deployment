import logging
import requests
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Insert your Azure Functions Endpoint and Bot Token
API_ENDPOINT = "https://dogclassfunctionapp.azurewebsites.net/api/azureDogClass" #replace with your own url
BOT_TOKEN = "Enter your bot token here" #replace with your bot token

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi there! Send me an image of either Frenchie, Pug or Boston Terrier and I will guess the type of breed.')

def predict_dog(update, context):
    """Send a photo of your dog"""
    logger.info('Predict Dog')
    img = update.message.photo[0].get_file()

    update.message.reply_text("🤖 Predict Dog AI function called...")
    update.message.reply_text("🚀🚀Little minions🧞 are rushing around for your answers🤔... 3️⃣...2️⃣...1️⃣...")
    # Send POST request to Endpoint
    files = {'file': img.download_as_bytearray()}
    r = requests.post(url=API_ENDPOINT, files=files)

    update.message.reply_text("🐶🎊✨✨🎊✨✨🎊✨✨🎊🐶\n" + "\n🤩And here is your answer!🤩\n\n" +r.text +"\n🦄🎈🎈🎆🎆🎈🎈🎆🎆🎈🎈🦄\n")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    logger.info("Starting bot")
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers 
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.photo, predict_dog))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot

    PORT = int(os.environ.get("PORT", "8443"))

    # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
    updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=BOT_TOKEN)
    
    #Replace your heroku url here
    updater.bot.set_webhook("https://<your_heroku_name.herokuapp.com/{}".format(BOT_TOKEN))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()