from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *


api = 'top secret'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_10 = KeyboardButton(text='Регистрация')
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
kb.row(button_10, button_1, button_2, button_3)


kb1 = InlineKeyboardMarkup()
button_4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.row(button_4, button_5)

kb2 = InlineKeyboardMarkup()
button_6 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_7 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_8 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_9 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.row(button_6, button_7)
kb2.row(button_8, button_9)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь уже существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer('Регистрация прошла успешно. Добро пожаловать!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    n = 1
    for p in products:
        await message.answer(f'Название: {p[0]} | Описание: {p[1]} | Цена: {p[2]}')
        with open(f'D:/pythonProgectsForUniversity/13-14_module_bot/img{n}.jpg', 'rb') as img:
            await message.answer_photo(img)
            n += 1
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора:\n'
                              '- для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n'
                              '- для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_sex(call):
    await call.message.answer('Введите свой пол (м/ж):')
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def set_age(message, state):
    await state.update_data(sex=message.text)
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['sex'] == 'ж':
        calorie_norm = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        await message.answer(f'Ваша норма - {calorie_norm} калорий в сутки')
    elif data['sex'] == 'м':
        calorie_norm = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        await message.answer(f'Ваша норма - {calorie_norm} калорий в сутки')
    else:
        await message.answer('Данные введены неверно. Попробуйте снова.')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Этот бот умеет рассчитывать калории для оптимального похудения или сохранения '
                         'нормального веса по формуле Миффлина-Сан Жеора.')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
