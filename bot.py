import asyncio
from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from inout import *
from calc import *
from logi import m_logging
from search import surename_search



TOKEN = '5871787475:AAFNwTES2xi0ZHrJVw1lb3wKZkz1934fQ7E'

class ActionStates(StatesGroup):
    calculator = State()
    calculator1 = State()
    phonebook = State()
    first_user_num = State()
    user_action = State()
    second_user_num = State()
    manual_input_st = State()
    read_st = State()
    search_st = State()
    import_st = State()
    uploaded_file_type_st = State()
    surename_input_st = State()
    phone_number_input_st = State()
    commentary_input_st = State()
    one_string_input_st = State()
    search_out = State()


bot_options = ['Калькулятор','Телефонная книга','cancel']
phone_book_options = ['Ручное внесение записей','Просмотр записей','Поиск по фамилии','cancel']
phone_book_view_options = ['В одну строку','В несколько строк','cancel']
calc_options = ['Вычисления','Логи','cancel']

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot,storage=storage)
clear_markup = types.ReplyKeyboardRemove()


def get_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Калькулятор'))
    return kb

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

def get_cancel():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('cancel'))

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Начало работы', reply_markup=make_row_keyboard(bot_options))

@dp.message_handler(Text(equals='cancel'), state='*')
async def cmd_cancel(message:types.Message, state: FSMContext):
    await message.reply('Работа отменена', reply_markup=clear_markup)
    await state.finish()

@dp.message_handler(Text(equals='Калькулятор'), state=None)
async def calc_select(message: types.Message):
    await ActionStates.calculator.set()
    await message.answer('Работа с калькулятором', reply_markup=make_row_keyboard(calc_options))

@dp.message_handler(Text(equals='Телефонная книга'), state=None)
async def phonebook_select(message: types.Message):
    await ActionStates.phonebook.set()
    await message.answer('Работа с телефонной книгой', reply_markup=make_row_keyboard(phone_book_options))

@dp.message_handler(Text(equals='Вычисления'), state=ActionStates.calculator)
async def start_calculation(message: types.Message, state: FSMContext):
    await ActionStates.first_user_num.set()
    await message.answer('Введите первое число', reply_markup=get_cancel())

@dp.message_handler(state=ActionStates.first_user_num)
async def get_first_user_number(message: types.Message, state: FSMContext):
    global f_u_n
    f_u_n = get_number(message.text)
    await state.set_state(ActionStates.user_action)
    await message.reply('Введите знак')

@dp.message_handler(state=ActionStates.user_action)
async def get_action(message: types.Message, state: FSMContext):
    global math_action
    math_action = message.text
    await state.set_state(ActionStates.second_user_num)
    await message.reply('Введите второе число')

@dp.message_handler(state=ActionStates.second_user_num)
async def get_second_user_number(message: types.Message, state: FSMContext):
    global s_u_n
    s_u_n = get_number(message.text)
    result = calculation(f_u_n, s_u_n, math_action)
    out_res = f'{f_u_n}{math_action}{s_u_n}={result}'
    m_logging(out_res)
    await message.reply(out_res, reply_markup=clear_markup)
    await state.finish()

@dp.message_handler(Text(equals='Логи'), state=ActionStates.calculator)
async def read_logi(message: types.Message, state: FSMContext):
    f = open('log.txt', 'r')
    logitxt = f.read
    await message.answer(logitxt(), reply_markup=clear_markup)
    f.close
    await state.finish()

@dp.message_handler(Text(equals='Ручное внесение записей'), state=ActionStates.phonebook)
async def phonebook_select_input_mode(message: types.Message, state: FSMContext):
    await ActionStates.manual_input_st.set()
    await message.answer('Выберите режим ввода', reply_markup=make_row_keyboard(phone_book_view_options))

@dp.message_handler(Text(equals='В одну строку'), state=ActionStates.manual_input_st)
async def string_pb_input(message: types.Message, state: FSMContext):
    await ActionStates.one_string_input_st.set()
    await message.answer('Введите фамилию, телефон, комментарий в одну строку через пробел', reply_markup=clear_markup)

@dp.message_handler(state=ActionStates.one_string_input_st)
async def get_first_user_number(message: types.Message, state: FSMContext):
    global string_input
    string_input = message.text
    add_strings(manual_input(string_input))
    await message.answer('Данные внесены', reply_markup=clear_markup)
    await state.finish()


@dp.message_handler(Text(equals='В несколько строк'), state=ActionStates.manual_input_st)
async def rows_pb_input(message: types.Message, state: FSMContext):
    await ActionStates.surename_input_st.set()
    await message.answer('Введите фамилию', reply_markup=clear_markup)

@dp.message_handler(state=ActionStates.surename_input_st)
async def get_first_user_number(message: types.Message, state: FSMContext):
    global surename
    surename = message.text
    await state.set_state(ActionStates.phone_number_input_st)
    await message.reply('Введите номер телефона')

@dp.message_handler(state=ActionStates.phone_number_input_st)
async def get_action(message: types.Message, state: FSMContext):
    global phonenumber
    phonenumber = message.text
    await state.set_state(ActionStates.commentary_input_st)
    await message.reply('Введите комментарий')

@dp.message_handler(state=ActionStates.commentary_input_st)
async def get_second_user_number(message: types.Message, state: FSMContext):
    global commentary
    commentary = message.text
    result = '; '.join([surename, phonenumber, commentary])
    add_strings(result)
    await message.answer('Данные внесены', reply_markup=clear_markup)
    await state.finish()

@dp.message_handler(Text(equals='Просмотр записей'), state=ActionStates.phonebook)
async def phonebook_select_read_mode(message: types.Message, state: FSMContext):
    await ActionStates.read_st.set()
    await message.answer('Выберите режим вывода', reply_markup=make_row_keyboard(phone_book_view_options))

@dp.message_handler(Text(equals='В одну строку'), state=ActionStates.read_st)
async def string_pb_output(message: types.Message, state: FSMContext):
    await message.answer('Вывод в одну строку', reply_markup=clear_markup)
    f = open('book.csv', 'r')
    booktxt = f.read
    await message.answer(booktxt(), reply_markup=clear_markup)
    f.close
    await state.finish()

@dp.message_handler(Text(equals='В несколько строк'), state=ActionStates.read_st)
async def rows_pb_output(message: types.Message, state: FSMContext):
    await message.answer('Вывод в несколько строк', reply_markup=clear_markup)
    f = open('book.csv', 'r')
    booktxt = f.read
    f.close
    await message.answer(output_rows(booktxt()))
    await state.finish()

@dp.message_handler(Text(equals='Поиск по фамилии'), state=ActionStates.phonebook)
async def phonebook_search_surename(message: types.Message, state: FSMContext):
    await ActionStates.search_st.set()
    await message.answer('Введите фамилию', reply_markup=clear_markup)

@dp.message_handler(state=ActionStates.search_st)
async def surename_input(message: types.Message, state: FSMContext):
    global search_result
    search_result = surename_search(message.text)
    await ActionStates.search_out.set()
    await message.answer('Выберите режим вывода', reply_markup=make_row_keyboard(phone_book_view_options))

@dp.message_handler(Text(equals='В одну строку'), state=ActionStates.search_out)
async def string_pb_output(message: types.Message, state: FSMContext):
    await message.answer('Вывод в одну строку', reply_markup=clear_markup)
    await message.answer(search_result, reply_markup=clear_markup)
    await state.finish()

@dp.message_handler(Text(equals='В несколько строк'), state=ActionStates.search_out)
async def rows_pb_output(message: types.Message, state: FSMContext):
    await message.answer('Вывод в несколько строк', reply_markup=clear_markup)
    await message.answer(output_rows(search_result))
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)