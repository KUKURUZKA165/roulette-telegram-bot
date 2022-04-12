from time import ctime
from random import randint
from asyncio import sleep
from config import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from requests import get
from algorithm import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup1.add(types.KeyboardButton("Випадковий факт"), types.KeyboardButton("Автор"), types.KeyboardButton("Грати"))
helpmsg = "<b>Ось список доступних команд:</b>\n\n<b>/roll</b> - Грати в рулетку (Також є на клавіатурі)\n\n<b>/orlanka</b> - Грати в орлянку (орел або решка)\n\n<b>/dice</b> - Підкинути кістки\n\n<b>/fact</b> - Випадковий факт про цього робота (Також є на клавіатурі)\n\n<b>/disclaimer</b> - Відмова від відповідальності\n\n<b>/author</b> - Автор бота (Також є на клавіатурі)\n\n<b>/ping</b> - Понг!\n\n<b>/keyboard</b> - Відкрити заново клавіатуру для гри\n\n<b>/rm_keyboard</b> - Закрити клавіатуру. Корисно у групах\n\n<b>/help</b> - Показати всі команди"

print(r"   ____                   ____              __     __  __            ____        __ ")
print(r"  / __ \____  ___  ____  / __ \____  __  __/ /__  / /_/ /____       / __ )____  / /_")
print(r" / / / / __ \/ _ \/ __ \/ /_/ / __ \/ / / / / _ \/ __/ __/ _ \     / __  / __ \/ __/")
print(r"/ /_/ / /_/ /  __/ / / / _, _/ /_/ / /_/ / /  __/ /_/ /_/  __/    / /_/ / /_/ / /_  ")
print(r"\____/ .___/\___/_/ /_/_/ |_|\____/\__,_/_/\___/\__/\__/\___/    /_____/\____/\__/   by @anton165")
print(r"    /_/                                                                             ")


async def log(text):
    print(text)
    with open('log.txt', 'a', encoding="utf-8") as file:
        file.write(f"\n{text}")


def randomorg_parse(number):
    site = get(f'https://www.random.org/integers/?num=1&min=1&max={number}&col=1&base=10&format=plain&rnd=new')
    randomorg_string = int("".join(c for c in site.text if c.isdecimal()))
    return randomorg_string


@dp.message_handler(commands=["start"])
async def start(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запитаний старт")

    send_mess = f"<b>Привіт, {message.from_user.first_name}! У цьому боті ти зможеш крутити рулетку.</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    send_mess = "<b>Оскільки бот безкоштовний, він не хоститься на віддаленому сервері. Через це я не можу тримати його увімкненим 24/7. Приношу свої вибачення!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    send_mess = "<b>Важливо для власників груп: </b>\nУ роботі обмежений доступ до повідомлень у групах на рівні Telegram API. Він не зможе за вами підглядати :)\n<b><a href='https://core.telegram.org/bots#privacy-mode'>Докладніше</a></b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", disable_web_page_preview=True)

    send_mess = helpmsg + "\n\n\n<b>Або користуйся клавіатурою з кнопками:</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    send_mess = "<b>🇺🇦 Слава Україні! 🇺🇦</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=markup1)

    await log("Старт відправлено!")


@dp.message_handler(commands=["roll"])
async def roll(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    send_mess = "<b>Очікування відповіді від random.org</b>"
    roll_mess = await bot.send_message(message.chat.id, send_mess, parse_mode="html", disable_web_page_preview=True)
    gamecode = randint(100, 999)
    await log(f"{gamecode} - Звернення до random.org...")

    rnd = randomorg_parse(37)
    result = fun_result(rnd)
    await log(f"{gamecode} - Результат - {result}.")
    await bot.edit_message_text(chat_id=message.chat.id, message_id=roll_mess.message_id, text=f"<b>{message.from_user.first_name}, ваш результат:\n{result}</b>", parse_mode="html", disable_web_page_preview=True)
    await log(f"{gamecode} - Готово.")


@dp.message_handler(commands=["ping"])
async def ping(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Пінг?")
    send_mess = f"<b>Понг! Я живий!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Понг!")


@dp.message_handler(commands=["disclaimer"])
async def disclaimer(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запитаний дисклеймер.")
    send_mess = "<b>ДИСКЛЕЙМЕР (ВІДМОВА ВІД ВІДПОВІДАЛЬНОСТІ): </b>Я повністю відмовляюся від результатів використання " \
                "даного бота не з метою розваги. Бот створений не з комерційною метою, і ніколи таким не " \
                "стане!\n\n<b>Коротко:</b> Ставок нема."
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Дисклеймер відправлено.")


@dp.message_handler(commands=["author"])
async def author(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запрошений автор.")
    send_mess = f"<b>🧑🏻‍💻 Мій автор - @anton165\nЙому можна давати ідеї для нових функцій у боті.</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Автор засланий)")


@dp.message_handler(commands=["keyboard"])
async def keyboard(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запрошено відкриття клавіатури!")
    send_mess = f"<b>Клавіатура відкрита!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=markup1)
    await log("Клавіатура відкрита.")


@dp.message_handler(commands=['rm_keyboard'])
async def rm_keyboard(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запитано закриття клавіатури!")
    send_mess = f"<b>Клавіатура закрита!</b>"
    await bot.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
    await log("Клавіатура закрита.")


@dp.message_handler(commands=["orlanka"])
async def orlanka(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    gamecode = randint(10, 99)
    send_mess = "<b>Очікування відповіді від random.org</b>"
    oreshka_mess = await bot.send_message(message.chat.id, send_mess, parse_mode="html", disable_web_page_preview=True)
    await log(f"{gamecode} - Запитана орлянка.")
    oreshka = randomorg_parse(2)

    resultoreshka = "Помилка. Скоріше за все проблема на стороні random.org"
    if oreshka == 1:
        await log(f"{gamecode} - Випав орел. Відправляю...")
        resultoreshka = "Орел"
    else:
        if oreshka == 2:
            await log(f"{gamecode} - Випала решка. Відправляю...")
            resultoreshka = "Решка"

    await bot.edit_message_text(chat_id=message.chat.id, message_id=oreshka_mess.message_id, text=f"<b>{message.from_user.first_name}, ваш результат:\n{resultoreshka}.</b>", parse_mode="html")
    await log("Надіслано.")


@dp.message_handler(commands=["dice"])
async def dice(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    gamecode = randint(10, 99)
    dice_sleep = 3
    await log(f"{gamecode} - Запрошений дайс.")
    dice_message = await bot.send_dice(message.chat.id, emoji="🎲")
    await log(f"{gamecode} - Підкинув. Результат: {dice_message.dice.value}. Чекаємо {dice_sleep} сек...")
    send_mess = f"<b>Зачекайте, будь ласка...</b>"
    dice_comment_message = await bot.send_message(message.chat.id, send_mess, parse_mode="html")

    dice_emoji = ""
    if dice_message.dice.value == 1:
        dice_emoji = "⚀"
    else:
        if dice_message.dice.value == 2:
            dice_emoji = "⚁"
        else:
            if dice_message.dice.value == 3:
                dice_emoji = "⚂"
            else:
                if dice_message.dice.value == 4:
                    dice_emoji = "⚃"
                else:
                    if dice_message.dice.value == 5:
                        dice_emoji = "⚄"
                    else:
                        if dice_message.dice.value == 6:
                            dice_emoji = "⚅"

    await sleep(dice_sleep)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=dice_comment_message.message_id, text=f"<b>{message.from_user.first_name}, ваш результат:\n{dice_emoji} {dice_message.dice.value}</b>", parse_mode="html")
    await log(f"{gamecode} - Готово.")


@dp.message_handler(commands=["fact"])
async def fact(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запитаний факт.")
    howmanyfacts = 5
    send_fact_mess = "Виникла помилка!"
    rnd_fact = randint(1, howmanyfacts)

    if rnd_fact == 1:
        send_fact_mess = f"Цей бот є FOSS проектом. Це означає, що його <a href='github.com/KUKURUZKA165/roulette-telegram-bot'>вихідний код</a> відкритий усім охочим. Будь-хто може перевірити чесність його роботи :)"
    else:
        if rnd_fact == 2:
            send_fact_mess = f"Випадковість у цьому роботі реалізована через атмосферний шум (random.org). Сучасні технології не здатні передбачити результат вашої гри."
        else:
            if rnd_fact == 3:
                send_fact_mess = f"Бот знає тільки {howmanyfacts} фактів себе. Він просто перебирає факти випадково і відправляє вам."
            else:
                if rnd_fact == 4:
                    send_fact_mess = f"Цей факт ще не придумали. Я не знаю що тут написати("
                else:
                    if rnd_fact == 5:
                        send_fact_mess = f"Навіть якби всі казино використовували такий самий спосіб отримання випадкових чисел, як у нас, вони все одно залишалися б у плюсі."

    await bot.send_message(message.chat.id, "<b>Цікавий факт:</b>\n" + send_fact_mess, parse_mode="html", disable_web_page_preview=True)

    await log(f"Я надіслав факт {rnd_fact} з {howmanyfacts}. Його зміст:\n{send_fact_mess}")


@dp.message_handler(commands=["help"])
async def help_command(message):
    await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-")
    await log("Запитана допомога")
    send_mess = helpmsg
    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
    await log("Готово")


@dp.message_handler(content_types=["text"])
async def mess(message):
    get_message_bot = message.text.strip().lower()

    if get_message_bot == "грати":
        await roll(message)
    else:
        if get_message_bot == "автор":
            await author(message)
        else:
            if get_message_bot == "випадковий факт":
                await fact(message)
            else:
                await log(f"--------------------\n{ctime()}\n{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username} id={message.from_user.id}\n{message.chat.title} {message.chat.invite_link} id = {message.chat.id}\n-\nПрислал(а): {message.text}")
                if message.from_user.id == message.chat.id:
                    send_mess = f"<b>Я вас не зрозумів :(</b>"
                    await bot.send_message(message.chat.id, send_mess, parse_mode="html")
                    await log("Надіслав користувачеві, що я його не зрозумів")


print(f"Доброго дня, Слава Україні!")

if __name__ == '__main__':
    executor.start_polling(dp)
