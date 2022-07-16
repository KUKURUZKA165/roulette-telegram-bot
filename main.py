from time import ctime, strftime
from random import randint
from asyncio import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession
from config import *

print(r"   ____                   ____              __     __  __            ____        __ ")
print(r"  / __ \____  ___  ____  / __ \____  __  __/ /__  / /_/ /____       / __ )____  / /_")
print(r" / / / / __ \/ _ \/ __ \/ /_/ / __ \/ / / / / _ \/ __/ __/ _ \     / __  / __ \/ __/")
print(r"/ /_/ / /_/ /  __/ / / / _, _/ /_/ / /_/ / /  __/ /_/ /_/  __/    / /_/ / /_/ / /_  ")
print(r"\____/ .___/\___/_/ /_/_/ |_|\____/\____/_/\___/\__/\__/\___/    /_____/\____/\__/  ")
print(r"    /_/                                                                             ")


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logfilename = f"log_{strftime(logfilename_date)}"

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
markup1.add(types.KeyboardButton("Випадковий факт ❓"),
            types.KeyboardButton("Дайс 🎲"),
            types.KeyboardButton("Закрити ❌"),
            types.KeyboardButton("Грати"))


async def log(text):
    print(text)
    if enablelog is True:
        with open(f'{logfoldername}/{logfilename}.txt', 'a', encoding="utf-8") as file:
            file.write(f"\n{text}")


async def logheader(msg):
    await log(f"--------------------\n{ctime()}\n"
              f"{msg.from_user.first_name} {msg.from_user.last_name} @{msg.from_user.username} id={msg.from_user.id}\n"
              f"{msg.chat.title} {msg.chat.invite_link} id={msg.chat.id}\n-")


async def randomorg_parse(minimum, maximum):
    async with ClientSession() as session:
        async with session.get(f"https://www.random.org/integers/"
                               f"?num=1&min={minimum}&max={maximum}&col=1&base=10&format=plain&rnd=new") as response:
            return int(await response.text())


@dp.message_handler(commands=["start"])
async def start(message):
    await logheader(message)
    await log("Запитаний старт")

    send_mess = f"<b>Привіт, {message.from_user.first_name}! У цьому боті ти зможеш крутити рулетку.</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    send_mess = "<b>Оскільки бот безкоштовний, він не хоститься на віддаленому сервері." \
                " Через це я не можу тримати його увімкненим 24/7. Приношу свої вибачення!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    send_mess = "<b>Важливо для власників груп: </b>\n" \
                "В бота налаштований обмежений доступ до повідомлень у групах на рівні Telegram API." \
                " Він не зможе за вами підглядати :)\n" \
                "<b><a href='https://core.telegram.org/bots#privacy-mode'>Докладніше</a></b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", disable_web_page_preview=True)

    send_mess = helpmsg + "\n\n\n<b>Або користуйся клавіатурою з кнопками:</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    send_mess = "<b>🇺🇦 Слава Україні! 🇺🇦</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=markup1)

    await log("Старт надіслано!")


@dp.message_handler(commands=["roll"])
async def roll(message):
    await logheader(message)
    send_mess = "<b>Очікування відповіді від random.org</b>"
    roll_mess = await bot.send_message(message.chat.id, send_mess, parse_mode="html", disable_web_page_preview=True)
    gamecode = randint(100, 999)
    await log(f"{gamecode} - Звернення до random.org...")

    num = await randomorg_parse(0, 36)
    if num == 0:
        result = "Зеро! 🟢 Зелений"
    elif num == 1 or num == 3 or num == 5 or num == 7 or num == 9 or num == 12 or num == 14 or num == 16 or num == 18\
            or num == 19 or num == 21 or num == 23 or num == 25 or num == 27 or num == 30 or num == 32 or num == 34\
            or num == 36:
        result = f"{num}, 🔴 Червоний"
    elif num == 2 or num == 4 or num == 6 or num == 8 or num == 10 or num == 11 or num == 13 or num == 15 or num == 17\
            or num == 20 or num == 22 or num == 24 or num == 26 or num == 28 or num == 29 or num == 31 or num == 33\
            or num == 35:
        result = f"{num}, ⚫ Чорний"
    else:
        result = "Помилка. Скоріше за все проблема на стороні random.org"

    await log(f"{gamecode} - Результат - {result}.")
    await bot.edit_message_text(chat_id=message.chat.id, message_id=roll_mess.message_id,
                                text=f"<b>{message.from_user.first_name}, ваш результат:\n{result}</b>",
                                parse_mode="html", disable_web_page_preview=True)
    await log(f"{gamecode} - Надіслано.")


@dp.message_handler(commands=["rnd"])
async def rnd_command(message):
    await logheader(message)
    await log("Запитаний rnd.")

    if message.text == "/rnd":
        await bot.send_message(message.chat.id, rnd_no_args, parse_mode="html")
        await log("Людина написала команду без аргументів.")
    else:
        minmax = message.text.replace("/rnd ", "")
        min_num, max_mun = minmax.split()
        min_num_int, max_mun_int = int(min_num), int(max_mun)

        send_mess = "<b>Очікування відповіді від random.org</b>"
        rnd_mess = await bot.send_message(message.chat.id, send_mess, parse_mode="html")

        if min_num_int >= 1000000000 or max_mun_int >= 1000000000 or min_num > max_mun:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=rnd_mess.message_id,
                                        text=rnd_something_went_wrong, parse_mode="html")
            await log("Людина неправильно вказала аргументи.")
        else:
            result = await randomorg_parse(min_num, max_mun)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=rnd_mess.message_id,
                                        text=f"<b>Мінімальне число: {min_num}\nМаксимальне число: {max_mun}\n\n"
                                             f"Результат: {result}</b>", parse_mode="html")
            await log(f"Вийшло {result} из {min_num} на {max_mun}")


@dp.message_handler(commands=["ping"])
async def ping(message):
    await logheader(message)
    await log("Пінг?")
    send_mess = "<b>Понг! Я живий!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Понг!")


@dp.message_handler(commands=["disclaimer"])
async def disclaimer(message):
    await logheader(message)
    await log("Запитаний дисклеймер.")
    await bot.send_message(message.chat.id, disclaimer_text, parse_mode="html")
    await log("Дисклеймер відправлено.")


@dp.message_handler(commands=["author"])
async def author(message):
    await logheader(message)
    await log("Запрошений автор.")
    send_mess = "<b>🧑🏻‍💻 Мій автор - @anton165\nЙому можна давати ідеї для нових функцій у боті.</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Автор засланий)")


@dp.message_handler(commands=["keyboard"])
async def keyboard(message):
    await logheader(message)
    await log("Запрошено відкриття клавіатури!")
    send_mess = "<b>Клавіатура відкрита!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=markup1)
    await log("Клавіатура відкрита.")


@dp.message_handler(commands=['rm_keyboard'])
async def rm_keyboard(message):
    await logheader(message)
    await log("Запитано закриття клавіатури!")
    send_mess = f"<b>Клавіатура закрита!</b>\nДля відкриття напишіть <b>/keyboard</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
    await log("Клавіатура закрита.")


@dp.message_handler(commands=["orlanka"])
async def orlanka(message):
    await logheader(message)
    gamecode = randint(10, 99)
    send_mess = "<b>Очікування відповіді від random.org</b>"
    oreshka_mess = await bot.send_message(message.chat.id, send_mess, parse_mode="html", disable_web_page_preview=True)
    await log(f"{gamecode} - Запитана орлянка.")
    oreshka = await randomorg_parse(1, 2)

    resultoreshka = "Помилка. Скоріше за все проблема на стороні random.org"
    if oreshka == 1:
        await log(f"{gamecode} - Випав орел. Відправляю...")
        resultoreshka = "Орел"
    elif oreshka == 2:
        await log(f"{gamecode} - Випала решка. Відправляю...")
        resultoreshka = "Решка"

    await bot.edit_message_text(chat_id=message.chat.id, message_id=oreshka_mess.message_id,
                                text=f"<b>{message.from_user.first_name}, ваш результат:\n{resultoreshka}.</b>",
                                parse_mode="html")
    await log(f"{gamecode} - Надіслано.")


@dp.message_handler(commands=["dice"])
async def dice(message):
    await logheader(message)
    gamecode = randint(10, 99)
    dice_sleep = 3
    await log(f"{gamecode} - Запрошений дайс.")
    dice_message = await bot.send_dice(message.chat.id, emoji="🎲")
    await log(f"{gamecode} - Підкинув. Результат: {dice_message.dice.value}. Чекаємо {dice_sleep} сек...")
    send_mess = "<b>Зачекайте, будь ласка...</b>"
    dice_comment_message = await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    dice_emoji = ""
    if dice_message.dice.value == 1:
        dice_emoji = "⚀"
    elif dice_message.dice.value == 2:
        dice_emoji = "⚁"
    elif dice_message.dice.value == 3:
        dice_emoji = "⚂"
    elif dice_message.dice.value == 4:
        dice_emoji = "⚃"
    elif dice_message.dice.value == 5:
        dice_emoji = "⚄"
    elif dice_message.dice.value == 6:
        dice_emoji = "⚅"

    await sleep(dice_sleep)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=dice_comment_message.message_id,
                                text=f"<b>{message.from_user.first_name}, ваш результат:\n{dice_emoji}"
                                     f" {dice_message.dice.value}</b>", parse_mode="html")
    await log(f"{gamecode} - Надіслано.")


@dp.message_handler(commands=["fact"])
async def fact(message):
    await logheader(message)
    await log("Запитаний факт.")
    send_fact_mess = "Виникла помилка!"
    rnd_fact = randint(1, howmanyfacts)

    if rnd_fact == 1:
        send_fact_mess = fact1
    elif rnd_fact == 2:
        send_fact_mess = fact2
    elif rnd_fact == 3:
        send_fact_mess = fact3
    elif rnd_fact == 4:
        send_fact_mess = fact4
    elif rnd_fact == 5:
        send_fact_mess = fact5

    await bot.send_message(message.chat.id, "<b>Цікавий факт:</b>\n" + send_fact_mess, parse_mode="html",
                           disable_web_page_preview=True)

    await log(f"Я надіслав факт {rnd_fact} з {howmanyfacts}. Його зміст:\n{send_fact_mess}")


@dp.message_handler(commands=["help"])
async def help_command(message):
    await logheader(message)
    await log("Запитана допомога")
    send_mess = helpmsg
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Готово")


@dp.message_handler(content_types=["text"])
async def mess(message):
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "грати":
        await log("--------------------\nКлавіатура:")
        await roll(message)
    elif get_message_bot == "закрити ❌":
        await log("--------------------\nКлавіатура:")
        await rm_keyboard(message)
    elif get_message_bot == "дайс 🎲":
        await log("--------------------\nКлавіатура:")
        await dice(message)
    elif get_message_bot == "випадковий факт ❓":
        await log("--------------------\nКлавіатура:")
        await fact(message)
    else:
        await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name}"
                  f" @{message.from_user.username} id={message.from_user.id}\n{message.chat.title}"
                  f" {message.chat.invite_link} id = {message.chat.id}\n-\nНадіслав(ла): {message.text}")
        if message.from_user.id == message.chat.id:
            send_mess = "<b>Я вас не зрозумів :(</b>"
            await bot.send_message(message.chat.id, send_mess, parse_mode="html")
            await log("Написав користувачеві, що я його не зрозумів")

if __name__ == '__main__':
    print("Доброго дня, Слава Україні!")
    executor.start_polling(dp)
