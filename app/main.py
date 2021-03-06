from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from app import messages
from exceptions import DoesNotExist, NotCorrectMessage
from menu import MenuManager
from settings import TELEGRAM_TOKEN
from users import UserManager

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


def auth(func):
    async def wrap(message):
        _id = message.from_user.id
        try:
            UserManager.get({'_id': _id})
            return await func(message)
        except DoesNotExist as err:
            await message.answer(str(err))

    return wrap


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.answer(messages.START_MESSAGE)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user = message.from_user
    try:
        UserManager.get({'_id': user.id})
    except DoesNotExist:
        UserManager.add(user)
    await message.answer(messages.START_MESSAGE, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['menu'])
@auth
async def menu_handler(message: types.Message):
    try:
        menu = MenuManager.get_current()
        await message.answer(menu)
    except DoesNotExist as err:
        await message.answer(str(err))


@dp.message_handler(commands=['set_menu'])
@auth
async def set_menu_handler(message: types.Message):
    UserManager.lock_command(message.from_user.id, 'set_menu')
    await message.answer("Send me new menu please 👀")


@dp.message_handler(commands=['order'])
@auth
async def order_handler(message: types.Message):
    # UserManager.lock_command(message.from_user.id, 'order')
    await bot.send_message(message.from_user.id, text='order pls')


@dp.message_handler()
async def update_menu(message: types.Message):
    try:
        user = UserManager.get({'_id': message.from_user.id})
        if getattr(user, 'command_lock', None) == 'set_menu':
            MenuManager.update_current(message.text)
            UserManager.unlock_command(user.id)
            await message.answer("Menu updated!🤌")
    except DoesNotExist:
        return
    except NotCorrectMessage as err:
        await message.answer(str(err))


if __name__ == '__main__':
    if TELEGRAM_TOKEN:
        executor.start_polling(dp, skip_updates=True)
    else:
        print('Telegram token is not defined.')
