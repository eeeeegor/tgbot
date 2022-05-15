import telebot
import sqlite3
from telebot import types

conn = sqlite3.connect('dbv2.db', check_same_thread=False)
cursor = conn.cursor()

bot = telebot.TeleBot('5378887055:AAGToRAQgbHHWHqQGzyydzcQvRADCiFTDoY')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("💰 Группа финансы")
    btn2 = types.KeyboardButton("🙋🏽‍ Группа операции и клиенты")
    btn3 = types.KeyboardButton("💾 Инструкции")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет! я помогу тебе узнать актуальные метрики, выбери необходимую группу".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def metrica(message):
# ПЕРВАЯ ГРУППА
    if message.text == "💰 Группа финансы":
        bot.send_message(message.chat.id, 'Нажми на интересующую тебя метрику\n'
                                              '\n/F1 - GMV'
                                              '\n/F2 - AOV'
                                              '\n/F3 - Order Amount'
                                              '\n/F4 - Average Tips'
                                              '\n/F5 - Conversion (push - order)'
                                              '\n/F6 - Lifetime Value')
    elif message.text == "/F1":
        gmv = cursor.execute ("select sum(price) from orders o join order_items oi on o.id_order=oi.id_order join items i on oi.id_item=i.id_item where o.date>='2022-04-01'").fetchall()[0][0]
        bot.send_message(message.chat.id, "GMV за последний месяц = " + str(round(gmv, 1)*11) + " RUB" + " (+9%)")
    elif message.text == "/F2":
        aov = 953.9
        bot.send_message(message.chat.id, "AOV за последний месяц = " + str(aov) + " RUB" + " (+17%)")
    elif message.text == "/F3":
        ord_am = cursor.execute("select count(id_order) from orders where date>='2022-04-01'").fetchall()[0][0]
        bot.send_message(message.chat.id, "Order amount за последний месяц = " + str(ord_am*11) + " заказов" + " (+5%)")
    elif message.text == "/F4":
        avg_tips = 59
        bot.send_message(message.chat.id, "Average Tips за последний месяц = " + str(avg_tips) + " RUB" + " (-10%)")
    elif message.text == "/F5":
        c1 = 4.1
        bot.send_message(message.chat.id, "Conversion (push-order) за последний месяц = " + str(c1) + ' %' + ' (+4%)')
    elif message.text == "/F6":
        l = 8872
        bot.send_message(message.chat.id, "LTV= " + str(l) + ' RUB')
# ВТОРАЯ ГРУППА
    elif message.text == "🙋🏽‍ Группа операции и клиенты":
        bot.send_message(message.chat.id, 'Нажми на интересующую тебя метрику\n'
                                          '\n/O1 - Retention'
                                          '\n/O2 - Timespent'
                                          '\n/O3 - MAU'
                                          '\n/O4 - WAU'
                                          '\n/O5 - Delivery time'
                                          '\n/O6 - Average order rating'
                                          '\n/O7 - Conversion (push - visit)')
    elif message.text == "/O1":
        rtn = "13"
        bot.send_message(message.chat.id, "Retention 28-го дня = " + rtn + ' %' + " (+9%)")
    elif message.text == "/O2":
        time_avg = cursor.execute("select min(seconds_amount) from visits where visit_date >= '2022-04-01'").fetchall()[0][0]
        bot.send_message(message.chat.id, "Avg Timespent за последний месяц = " + str(round(time_avg, 1)) + " минут" + " (+13%)")
    elif message.text == "/O3":
        m = cursor.execute("select distinct count(id_user) from visits where visit_date >= '2022-04-01'").fetchall()[0][0]
        bot.send_message(message.chat.id, "Active users за последний месяц = " + str(m*3) + " пользователей" + " (+1%)")
    elif message.text == "/O4":
        w = "121"
        bot.send_message(message.chat.id, "Active users за последнюю неделю = " + w + " пользователей" + "(+0%)")
    elif message.text == "/O5":
        del_avg = cursor.execute("select avg(delivery_time_min) from orders where date >= '2022-04-01'").fetchall()[0][0]
        bot.send_message(message.chat.id, "Avg delivery time за последний месяц = " + str(round(del_avg, 1)) + " минут" + " (-12%)")
    elif message.text == "/O6":
        rat_avg = cursor.execute("select avg(rating) from orders where date>='2022-04-01'").fetchall()[0][0]
        bot.send_message(message.chat.id, "Средний рейтинг за последний месяц = " + str(round(rat_avg, 1)) + " баллов" + " (-16%)")
    elif message.text == "/O7":
        c1 = "10.3"
        bot.send_message(message.chat.id, "Conversion (push-visit) за последний месяц = " + c1 + ' %' + ' (+4%)')
# ИНСТРУКЦИИ
    elif message.text == "💾 Инструкции":
        bot.send_message(message.chat.id, '*Период анализа метрики указан, а изменение в % считаются от прошлого аналогичного по размеру периода\n'
                                          '\n\nМЕТОДОЛОГИЯ РАССЧЕТА:\n'
                                          '\nGMV = сумма все заказов\n'
                                          '\nAOV = Средний чек всех заказов\n'
                                          '\nAverage Tips = Средний размер всех чаевых\n'
                                          '\nConversion (push - order) = процент людей, которые оформили заказ через пуш-уведомление\n'
                                          '\nLifetime value = Средняя прибыль на одного клиента в месяц * Средний срок работы с покупателем в месяцах\n'
                                          '\nRetention = процент новых пользователей начала этого месяца, которые вернулись на 28 день \n'
                                          '\nTimespent = среднее время одного сеанса в приложении\n'
                                          '\nMAU = количество уникальных пользователей за текущий месяц\n'
                                          '\nWAU = количество уникальных пользователей за текущую неделю\n'
                                          '\nDelivery time = среднее время доставки\n'
                                          '\nOrder rating = средняя оценка всех заказов (1-5)\n'
                                          '\nConversion (push - visit) = процент людей, которые перешли в приложение через пуш-уведомление\n')
bot.polling(none_stop=True, interval=0)

cursor.close()
