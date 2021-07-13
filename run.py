import logging
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
from API import api

bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Хабарлама типі
msg = types.Message

@dp.message_handler(commands=['start'])
async def command_start(message: msg):
    id_user = message.from_user.id
    start_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    start_btn.add("Сілтеме жіберу")
    await bot.send_message(message.from_user.id,
                           "Сайтқа сілтеме жіберіңіз⬆",
                           reply_markup=start_btn)

from forma import Forma
@dp.message_handler(state='*', commands='Бас тарту🙌🏻')
@dp.message_handler(Text(equals='Бас тарту🙌🏻', ignore_case=True), state='*')
async def cancell_handler(message: types.Message, state: FSMContext):
    """
    :param message: Бастартылды
    :param state: Тоқтату
    :return: finish

    """

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Бас тарту!')
    await state.finish()
    main_btn = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    main_btn.add("Сілтеме жіберу")
    await message.reply('Бастартылды.', reply_markup=main_btn)

@dp.message_handler(content_types=['text'])
async def content_text(message: msg):
    public_m = message.text

    if public_m == "Сілтеме жіберу":
        await Forma.link.set()
        cancell = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        cancell.add("Бас тарту🙌🏻")
        await bot.send_message(message.from_user.id,
                               "Сайтқа сілтеме жіберіңіз⬆",
                               reply_markup=cancell)
    else:
        await bot.send_message(message.from_user.id,
                               "/start басыңыз")


from pkgCelery import parse
from db import connection, cursor, insert, check_url
@dp.message_handler(state=Forma.link)
async def start_state(message: msg, state: FSMContext):
    id_u = message.from_user.id
    global link_
    async with state.proxy() as data:
        data['link'] = message.text
        link_ = data['link']
    print(link_)
    '''
    тексеру!
    '''
    #t = check_url(link_)
    check = "SELECT res FROM links WHERE URLS = %s"
    cursor.execute(check, (link_,))
    c = cursor.fetchall()
    for i in c:
        l = int(''.join(map(str, i)))
        await bot.send_message(message.from_user.id,
                               text="Сіздің жіберген сілтемеңіз базада🗂 бар😊, тэгтер саны: {}".format(l),
                               reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                      selective=True).add("Сілтеме жіберу"))
        break



    else:
        await bot.send_message(message.from_user.id,
                               text="Тапсырма дайын емес, күте тұрыңыз🙃")
        res = parse(link_)
        insert(id_u, link_, res)
        await bot.send_message(message.from_user.id,
                               text="Тэгтер саны: {}".format(res),
                               reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                      selective=True
                                                                      ).add("Сілтеме жіберу"))

    await state.finish()
    

if __name__ == "__main__":
    '''
    Запуск
    '''
    from aiogram.utils import executor
    executor.start_polling(dp, skip_updates=True)

