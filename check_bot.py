from random import randint
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from son_top import sonTopUser, updateResult, compGenerateNumber, updateCompResult

logging.basicConfig(level=logging.INFO)

TOKEN = "6171836779:AAEO3u3Sj0fFUPdXWQw9RZsn4p-gPRdcNpo"

bot = Bot(TOKEN)
dp = Dispatcher(bot)
result = {
    'urinish': 0,
    'ok': False,
    'kattami': None,
    'number': randint(1, 10)
}

result_bot = {
    'urinish': 0,
    'ok': False,
    'halol': True,
    'a': 1,
    'b': 10,
    'number': randint(1, 10)
}

result_game = {
    'user': result['urinish'],
    'computer': result_bot['urinish']
}

# buttons
startGameButton = KeyboardButton("O'yinni boshlash")
qwerty = KeyboardButton("Siz o'ylagan")

startUserButton = KeyboardButton("Lets go!")

kattaButton = KeyboardButton("Katta")
kichikButton = KeyboardButton("Kichik")
togriButton = KeyboardButton("To'g'ri")

# replyKeyboardButtons
gameReplyMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(startGameButton)

userReplyMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(startUserButton)

gameloopMarkup = ReplyKeyboardMarkup(resize_keyboard=True).row(kichikButton, kattaButton, togriButton)


@dp.message_handler(commands=['start'])
async def startMessage(msg: types.Message):
    await msg.reply("O'yin botiga xush kelibsiz👋", reply_markup=gameReplyMarkup)


@dp.message_handler(commands=['help'])
async def startMessage(msg: types.Message):
    await msg.reply("O'yinni boshlash uchun Boshlashni bosing✅", reply_markup=gameReplyMarkup)


@dp.message_handler(text_contains='O\'yinni boshlash')
async def startGame(msg: types.Message):
    updateResult(result)
    await msg.answer("Men 1dan 10gacha bo'lgan sonni o'yladim uni topingchi❗️", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text_contains='Lest go!')
async def startUserGame(msg: types.Message):
    updateCompResult(result_bot)
    comp_son = result_bot['number']
    await msg.answer(f"Siz {comp_son} sonini o'yladingiz❗️", reply_markup=gameloopMarkup)


@dp.message_handler(text_contains='Katta')
async def kattaUserGame(msg: types.Message):
    res = compGenerateNumber('+', result_bot)
    if res['halol']:
        comp_son = res['number']
        await msg.answer(f"Siz {comp_son} sonini o'yladingiz✅", reply_markup=gameloopMarkup)
    else:
        await msg.reply("Siz halol o'ynamadingiz, shuning uchun siz yutqazdingiz😒", reply_markup=gameReplyMarkup)


@dp.message_handler(text_contains='Kichik')
async def kattaUserGame(msg: types.Message):
    res = compGenerateNumber('-', result_bot)
    if res['halol']:
        comp_son = res['number']
        await msg.answer(f"Siz {comp_son} sonini o'yladingiz❗️", reply_markup=gameloopMarkup)
    else:
        await msg.reply("Siz halol o'ynamadingiz, shuning uchun siz yutqazdingiz😒", reply_markup=gameReplyMarkup)


@dp.message_handler(text_contains='To\'g\'ri')
async def kattaUserGame(msg: types.Message):
    res = compGenerateNumber('t', result_bot)
    result_game['computer'] = res['urinish']
    await msg.answer(f"O'zimga qoyil men siz o'ylagan sonni {res['urinish']} ta urinishda topdim!")
    if result_game['user'] > result_game['computer']:
        await msg.answer(f"Va bu o'yinda men yutdim!", reply_markup=gameReplyMarkup)
    elif result_game['user'] < result_game['computer']:
        await msg.answer(f"Lekin bu o'yinda siz yutdingiz!", reply_markup=gameReplyMarkup)
    else:
        await msg.answer(f"Durrang do'stlik g'alaba qozondi😁", reply_markup=gameReplyMarkup)


@dp.message_handler()
async def numberResult(msg: types.Message):
    son = msg.text
    if result['ok']:
        await msg.reply("Davom etish uchun Lets go! tugmasini bosing✅")
    else:
        if len(son.split()) > 1:
            await msg.answer("Qayta jo'nating❗")
        else:
            if son.isdigit():
                son = int(son)
                res = sonTopUser(son, result)
                if res['ok']:
                    result_game['user'] = res['urinish']
                    await msg.answer(f"Qoyil siz topdingiz va {res['urinish']} ta urinish amalgan oshirdingiz!")
                    await msg.answer(f"Endi siz bir son o'ylang men topishga harakat qilaman.",
                                     reply_markup=userReplyMarkup)
                else:
                    await msg.answer(f"Men o'ylagan son bundan {'katta' if res['kattami'] else 'kichik'}.")
            else:
                await msg.reply("Siz son yubormadingiz❗️")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
