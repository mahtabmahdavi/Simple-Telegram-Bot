import random
import telebot
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode


bot = telebot.TeleBot("TOKEN", parse_mode = None)


@bot.message_handler(commands = ["start"])
def start(message):
    bot.reply_to(message, message.from_user.first_name + " خوش آمدی")


@bot.message_handler(commands = ["help"])
def help(message):
    bot.reply_to(message, """/start
خوش‌آمد گویی 🎉✨
/game
بازی حدس اعداد رو با این می‌تونی بازی کنی.\n
/age
تاریخ تولدت رو با فرمت "1376/9/9" وارد کن، سنت رو خیلی دقیق ببین.\n
/voice
یه جملۀ انگلیسی به من می‌دی، منم اون رو به صورت voice بهت می‌دم.\n
/max
یه آرایه با فرمت "14,7,78,15,8,19,20" به من می‌دی، منم بهت می‌گم بزرگ‌ترین عدد آرایه‌ت کدومه.\n
/argmax
یه آرایه با فرمت "14,7,78,15,8,19,20" به من می‌دی، منم بهت می‌گم بزرگ‌ترین عدد تو خونۀ چندمه.\n
/qrcode
متن خودت رو به من می‌دی، منم QR code اون رو بهت می‌دم.\n
/help
برای کمک به تو اینجام 🥰""")


@bot.message_handler(commands = ["game"])
def game(message):
    global randomNumber
    randomNumber = random.randint(1, 100)
    userMessage = bot.send_message(message.chat.id, "قراره یه عدد بین 1 تا 100 رو حدس بزنی. حالا حدست رو وارد کن.")
    bot.register_next_step_handler(userMessage, gameHelper)


def gameHelper(message):
    global randomNumber

    try:
        if message.text == "New Game 🎮":
            randomNumber = random.randint(1, 100)
            userMessage = bot.send_message(message.chat.id, "دوباره بازی رو شروع می‌کنیم.\nحدست رو وارد کن.")
            bot.register_next_step_handler(userMessage, gameHelper)

        elif int(message.text) < randomNumber:
            userMessage = bot.send_message(message.chat.id, "برو بالا ⬆", reply_markup = markup)
            bot.register_next_step_handler(userMessage, gameHelper)

        elif int(message.text) > randomNumber:
            userMessage = bot.send_message(message.chat.id, "برو پایین ⬇", reply_markup = markup)
            bot.register_next_step_handler(userMessage, gameHelper)

        elif int(message.text) == randomNumber:
            bot.send_message(message.chat.id, "برنده شدی 🥳", reply_markup = telebot.types.ReplyKeyboardRemove(selective = True))
            
    except:
        userMessage = bot.send_message(message.chat.id, "عدد وارد نکردی، لطفاً یه عدد بین 1 تا 100 رو وارد کن.")
        bot.register_next_step_handler(userMessage, gameHelper)


@bot.message_handler(commands = ["age"])
def age(message):
    userMessage = bot.send_message(message.chat.id, "تاریخ تولدت رو با فرمت \"1376/9/9\" وارد کن.")
    bot.register_next_step_handler(userMessage, calculateAge)


def calculateAge(message):
    try:
        birthDate = message.text.split("/")
        difference = JalaliDatetime.now() - JalaliDatetime(birthDate[0], birthDate[1], birthDate[2])
        year = difference.days // 365
        difference = difference.days % 365
        month = difference // 30
        day = difference % 30 - 7
        bot.send_message(message.chat.id, "تو " + str(year) + " سال و " + str(month) + " ماه و " + str(day) + " روزه هستی.")
    except:
        userMessage = bot.send_message(message.chat.id, "حتماً باید تاریخ تولدت رو با فرمت بالا وارد کنی.")
        bot.register_next_step_handler(userMessage, calculateAge)


@bot.message_handler(commands = ["voice"])
def voice(message):
    userMessage = bot.send_message(message.chat.id, "یه جملۀ انگلیسی بنویس.")
    bot.register_next_step_handler(userMessage, voiceMaker)


def voiceMaker(message):
    try:
        language = "en"
        voiceMessage = gTTS(text = message.text, lang = language, slow = False)
        voiceMessage.save("voice.mp3")
        voiceFile = open("voice.mp3", "rb")
        bot.send_voice(message.chat.id, voiceFile)
    except:
        userMessage = bot.send_message(message.chat.id, "فقط متن وارد کن نه چیز دیگه!")
        bot.register_next_step_handler(userMessage, voiceMaker)


@bot.message_handler(commands = ["max"])
def maximum(message):
    userMessage = bot.send_message(message.chat.id, "قراره بزرگ‌ترین عدد تو یه آرایه رو پیدا کنم.\nآرایۀ مورد نظرت رو طبق فرمت \"14,7,78,15,8,19,20\" وارد کن.")
    bot.register_next_step_handler(userMessage, maxNumber)


def maxNumber(message):
    try:
        numbers = list(map(int, message.text.split(",")))
        maximum = max(numbers)
        bot.reply_to(message, "بزرگ‌ترین عدد " + str(maximum) + " هست.")
    except:
        userMessage = bot.send_message(message.chat.id, "اشتباه وارد کردی!\nلطفاً اعداد رو با فرمت \"14,7,78,15,8,19,20\" وارد کن.")
        bot.register_next_step_handler(userMessage, maxNumber)


@bot.message_handler(commands = ["argmax"])
def argmax(message):
    userMessage = bot.send_message(message.chat.id, "قراره موقعیت بزرگ‌ترین عدد تو یه آرایه رو پیدا کنم.\nآرایۀ مورد نظرت رو طبق فرمت \"14,7,78,15,8,19,20\" وارد کن.")
    bot.register_next_step_handler(userMessage, maxIndex)


def maxIndex(message):
    try:
        numbers = list(map(int, message.text.split(",")))
        index = numbers.index(max(numbers))
        bot.reply_to(message, "بزرگ‌ترین عدد در موقعیت " + str(index + 1) + " قرار داره.")
    except:
        userMessage = bot.send_message(message.chat.id, "اشتباه وارد کردی!\nلطفاً اعداد رو با فرمت \"14,7,78,15,8,19,20\" وارد کن.")
        bot.register_next_step_handler(userMessage, maxIndex)


@bot.message_handler(commands = ["qrcode"])
def QRcode(message):
    userMessage = bot.send_message(message.chat.id, "متن خودت رو وارد کن.")
    bot.register_next_step_handler(userMessage, QRcodeMaker)


def QRcodeMaker(message):
    if isinstance(message.text, str) == True:
        qrcodeImage = qrcode.make(message.text)
        qrcodeImage.save("QR.jpg")
        qrcodeFile = open("QR.jpg", "rb")
        bot.send_photo(message.chat.id, qrcodeFile)
    else:
        userMessage = bot.send_message(message.chat.id, "فقط متن وارد کن نه چیز دیگه!")
        bot.register_next_step_handler(userMessage, QRcodeMaker)


markup = telebot.types.ReplyKeyboardMarkup(row_width = 1)
button = telebot.types.KeyboardButton("New Game 🎮")
markup.add(button)

bot.infinity_polling()