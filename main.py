import telebot
from telebot import types

import settings
from commands import MAKE_ORDER, UPDATE_MENU, QUIT, GET_MENU
from database import get_db_data, update_db

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

MENU_DELIMITER = '——'

def command_is_locked(user, command):
    data = get_db_data()
    return data['commands_in_progress'].get(str(user.id)) == command


def lock_command(user, command):
    data = get_db_data()
    data['commands_in_progress'].update({str(user.id): command})
    update_db(data)


def remove_command_lock(user):
    data = get_db_data()
    data['commands_in_progress'].pop(str(user.id))
    update_db(data)


def lock_command_decorator(command):
    def decorator(fun):
        def wrapper(message):
            lock_command(message.from_user, command)
            return fun(message)
        return wrapper
    return decorator


def update_menu(menu_text):
    data = get_db_data()
    menu = [i.split('\n') for i in menu_text.split(f'\n{MENU_DELIMITER}\n')]
    data['menu'] = menu
    update_db(data)


@bot.message_handler(commands=['start'], chat_types=['private'])
def start(message):
    data = get_db_data()
    user = message.from_user
    data['users'].update({str(user.id): message.json['from']})
    data['users_id_list'].append(str(user.id))
    data['users_id_list'] = list(set(data['users_id_list']))
    update_db(data)

    # setup keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton(MAKE_ORDER))
    if user.username in settings.ADMIN_LIST:
        markup.add(types.KeyboardButton(UPDATE_MENU))
    bot.send_message(message.chat.id, f'Welcome aboard {user.first_name}', reply_markup=markup)


@bot.message_handler(content_types=['text'], chat_types=['private'])
def message_handler(message):
    user = message.from_user
    if message.text == UPDATE_MENU:
        lock_command(user, UPDATE_MENU)
        bot.send_message(message.chat.id, 'Send me new menu please 👀')
    if command_is_locked(user, UPDATE_MENU):
        update_menu(menu_text=message.text)
        remove_command_lock(user)


@bot.message_handler(commands=[UPDATE_MENU], chat_types=['private'])
@lock_command_decorator(UPDATE_MENU)
def update_menu_handler(message):
    bot.send_message(message.chat.id, 'Send me new menu please 👀')


def make_order(message):
    pass


def load_orders(message):
    pass


@bot.message_handler(commands=[GET_MENU])
def get_menu_handler(message):
    data = get_db_data()
    menu_list = ['\n'.join(i) for i in data['menu']]
    menu_list_with_delimiter = '\n——\n'.join(menu_list)
    bot.send_message(message.chat.id, menu_list_with_delimiter)


@bot.message_handler(commands=[QUIT])
def quit_handler(message):
    user = message.from_user
    data = get_db_data()
    data['users'].pop(str(user.id))
    data['commands_in_progress'].pop(str(user.id))
    data['users_id_list'] = list(filter(lambda x: x != str(user.id), data['users_id_list']))

    # remove keyboard
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'Bye {user.first_name} 😞', reply_markup=markup)


bot.polling(none_stop=True)
