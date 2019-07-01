from flask import Flask, request
import telebot
import pyowm
import os

owm = pyowm.OWM('bd4020999b62f43d52b17e4684c59965')
bot = telebot.TeleBot("780352854:AAHXCsAW4SJi1juBgJ6JZ_vbPXafsCU2DKI")
server = Flask(__name__)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')["temp"]

        answer = f"\nWeather in {str.upper(message.text)}: {str.title(w.get_detailed_status())}"
        answer += f"\nThe temperature is {str(temp)} °C\n\n"

        if temp < 10:
            answer += "It's too cold, dress very warmly.\n"
        elif temp < 20:
            answer += "It's still not warm, dress a little warmly.\n"
        elif temp < 25:
            answer += "The temperature is OK, wear anything you want.\n"
        else:
            answer += "It's hot outside, wear light clothes.\n"

        answer += "____________________________________\n"
        answer += " Weather-Bot by Vahan Sahakyan.\n"

        bot.send_message(message.chat.id, answer)
    except pyowm.exceptions.api_response_error.NotFoundError:
        notFoundMessage = f"Oops..!\n" \
            f"There's no information\n" \
            f"about \"{message.text}\".\n\n" \
            f"Enter another location.\n"\
            f"(Correct spelling mistakes)" \

        bot.send_message(message.chat.id, notFoundMessage)

bot.polling(none_stop=True)

@server.route('/' + owm, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://pure-plains-88780.herokuapp.com/' + owm)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


