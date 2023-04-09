import os

from aiogram import types

from localizations.ru_localization import CMD_START_MESSAGE, CMD_HELP_MESSAGE, CMD_DELETE_MESSAGE, CMD_STATS_MESSAGE
from repositories import db_repo as db
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import mainKeyboard, get_profileKeyboard, cancelKeyboard, startKeyboard, statsKeyboard
from main import dp, bot
from utils.stats_calc import get_sum_expenses_and_incomes_for_period, get_expenses_category_graphic, \
    get_expenses_graphic_by_days, get_incomes_graphic_by_days


class RegisterStatesGroup(StatesGroup):
    balance = State()


class DeleteUserStatesGroup(StatesGroup):
    confirm = State()


class SetUserBalanceStatesGroup(StatesGroup):
    balance = State()


@dp.message_handler(commands=['cancel'], state="*")
async def cancel_state(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы отменили действие!', reply_markup=mainKeyboard)


# ========================= REGISTER =========================


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_is_exist = await db.user_is_exist(message.from_user.id)
    if user_is_exist:
        await message.answer('Да-да, что-то хотел? Отправь мне /help для просмотра функционала бота!',
                             reply_markup=mainKeyboard)
    else:
        await message.answer(CMD_START_MESSAGE, parse_mode='HTML')
        await RegisterStatesGroup.balance.set()


@dp.message_handler(regexp=r"\D", state=RegisterStatesGroup.balance)
async def handle_register_balance_check(message: types.Message):
    await message.answer('⛔️ Ошибка. Введи сумму в виде числа без знаков, к примеру 2500.')


@dp.message_handler(regexp=r"\d", state=RegisterStatesGroup.balance)
async def handle_register_balance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['balance'] = message.text
    await message.answer('Отлично! Твой баланс установлен. Теперь ты можешь ввести /help, '
                         'чтобы узнать основные команты. Успеха!', reply_markup=mainKeyboard)
    await db.add_user(message.from_user.id, state)
    await state.finish()


# ========================= BALANCE =========================


@dp.message_handler(text='Баланс')
async def set_balance(message: types.Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(f'💰 Твой баланс: {user.balance} ₽')


@dp.callback_query_handler(lambda cb: cb.data == 'set_balance')
async def cmd_set_balance(callback: types.CallbackQuery):
    await callback.message.answer('📍 Так, давай установим тебе новый баланс. Напиши чему он должен равняться:',
                                  reply_markup=cancelKeyboard)
    await SetUserBalanceStatesGroup.balance.set()
    await callback.answer(' ')


@dp.message_handler(regexp=r"\D", state=SetUserBalanceStatesGroup.balance)
async def cmd_set_balance_check(message: types.Message):
    await message.answer('⛔️ Ошибка. Введи сумму в виде числа без знаков, к примеру 2500.')


@dp.message_handler(regexp=r"\d", state=SetUserBalanceStatesGroup.balance)
async def handle_cmd_set_balance(message: types.Message, state: FSMContext):
    async with state.proxy():
        await db.update_user_balance(user_id=message.from_user.id, balance=message.text)
    await message.answer('✅ Отлично! Твой баланс установлен.', reply_markup=mainKeyboard)
    await state.finish()


# ========================= STATS AND PROFILE CMD =========================


@dp.message_handler(text='Статистика')
async def cmd_stats(message: types.Message):
    user = await db.get_user(message.from_user.id)
    user_stat = await get_sum_expenses_and_incomes_for_period(user_id=message.from_user.id)
    filename = await get_expenses_category_graphic(message.from_user.id)
    print(filename)
    with open(filename, 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo,
                             caption=CMD_STATS_MESSAGE(user.balance, user_stat),
                             parse_mode='HTML', reply_markup=statsKeyboard)
        os.remove(filename)


@dp.message_handler(text='Профиль')
async def cmd_profile(message: types.Message):
    user_notice = (await db.get_user(message.from_user.id)).notice
    await message.answer(f'👤 Настройки твоего профиля:', reply_markup=get_profileKeyboard(user_notice))


@dp.message_handler(text='Доходы')
async def cmd_incomes(message: types.Message):
    filename = await get_incomes_graphic_by_days(message.from_user.id)
    if filename != 'Error':
        with open(filename, 'rb') as photo:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo)
            os.remove(filename)
    else:
        await message.answer(f'❌ Операций нет!', reply_markup=statsKeyboard)


@dp.message_handler(text='Расходы')
async def cmd_expenses(message: types.Message):
    filename = await get_expenses_graphic_by_days(message.from_user.id)
    if filename != 'Error':
        with open(filename, 'rb') as photo:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo)
            os.remove(filename)
    else:
        await message.answer(f'❌ Операций нет!', reply_markup=statsKeyboard)


# ========================= EDIT NOTICE =========================

@dp.callback_query_handler(lambda cb: cb.data == 'notice_toggle')
async def notice_toggler(callback: types.Message):
    await db.update_user_notice(callback.from_user.id)
    user_notice = await db.get_user(callback.from_user.id)
    await bot.edit_message_text(f'👤 Настройки твоего профиля:', reply_markup=get_profileKeyboard(user_notice.notice))


# ========================= DELETE PROFILE =========================


@dp.callback_query_handler(lambda callback: callback.data == 'delete_user')
async def cmd_delete(callback: types.CallbackQuery):
    await callback.message.answer(CMD_DELETE_MESSAGE, reply_markup=cancelKeyboard)
    await callback.answer()
    await DeleteUserStatesGroup.confirm.set()


@dp.message_handler(state=DeleteUserStatesGroup.confirm)
async def cmd_delete_confirm(message: types.Message, state: FSMContext):
    if message.text == '/delete':
        await db.delete_user(message.from_user.id)
        await message.answer('Все данные о тебе стёрты! Введи /start, чтобы начать с чистого листа.',
                             reply_markup=startKeyboard)
    else:
        await message.answer('Действие отмененно.')
    await state.finish()


# ========================= OTHER =========================


@dp.message_handler(commands=['help'])
async def cancel_state(message: types.Message):
    await message.answer(CMD_HELP_MESSAGE, parse_mode='HTML')


@dp.message_handler(text='Назад')
async def cmd_back(message: types.Message):
    await message.answer(f'🪧 Ты снова в главном меню!', reply_markup=mainKeyboard)
