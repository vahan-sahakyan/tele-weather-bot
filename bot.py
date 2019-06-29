import telebot
import pyowm

owm = pyowm.OWM('bd4020999b62f43d52b17e4684c59965')
bot = telebot.TeleBot("780352854:AAHXCsAW4SJi1juBgJ6JZ_vbPXafsCU2DKI")


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
