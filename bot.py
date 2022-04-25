import telebot

bot = telebot.TeleBot('5258860993:AAFfdF8myYlunCrz8JaT-zws6Lpkejs0T4Q')
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет, как тебя зовут?)')
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, message.text + ', иди')
bot.polling(none_stop=True, interval=0)

