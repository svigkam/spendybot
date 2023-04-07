import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import mainKeyboard, addIncomeKeyboard, addExpenseKeyboard, cancelKeyboard

from repositories import db_repo as db
from main import dp

income_cats = [
    'SALARY', 'PRESENT', 'OTHER', 'OVERWORK'
]


class AddIncomeStatesGroup(StatesGroup):
    category = State()
    amount = State()


class AddExpenseStatesGroup(StatesGroup):
    amount = State()
    category = State()


# ======================= ADD INCOME =======================

@dp.message_handler(text='Добавить доход')
async def add_income(message: types.Message):
    await message.answer('📍 Выбери источник дохода:', reply_markup=addIncomeKeyboard)
    await message.answer('🍁 Для отмены ты можешь написать мне /cancel', reply_markup=cancelKeyboard)
    await AddIncomeStatesGroup.category.set()


@dp.callback_query_handler(lambda call: call.data in income_cats, state=AddIncomeStatesGroup.category)
async def add_income_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = callback.data
    await callback.message.delete()
    await callback.message.answer('📍 Отлично, а теперь введи сумму: ', reply_markup=cancelKeyboard)
    await AddIncomeStatesGroup.amount.set()
    await callback.answer()


@dp.message_handler(regexp=r"\D", state=AddIncomeStatesGroup.amount)
async def add_income_amount_check(message: types.Message, state: FSMContext):
    await message.answer('⛔️ Ошибка. Введи сумму в виде числа без знаков, к примеру 2500.')


@dp.message_handler(regexp=r"\d", state=AddIncomeStatesGroup.amount)
async def add_income_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await db.add_income_operation(message.from_user.id, state)
    await message.answer('✅ Доход успешно добавлен!', reply_markup=mainKeyboard)
    await state.finish()


# ======================= ADD EXPENSE =======================

@dp.message_handler(text='Добавить покупку')
async def add_expense(message: types.Message):
    await message.answer('📍 Выбери категорию твоей покупки:', reply_markup=addExpenseKeyboard)
    await message.answer('🍁 Для отмены ты можешь написать мне /cancel', reply_markup=cancelKeyboard)
    await AddExpenseStatesGroup.category.set()


@dp.callback_query_handler(state=AddExpenseStatesGroup.category)
async def add_expense_category(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = callback.data
    await callback.message.delete()
    await callback.message.answer('📍 Теперь введи стоимость покупки:')
    await AddExpenseStatesGroup.amount.set()
    await callback.answer()


@dp.message_handler(regexp=r"\D", state=AddExpenseStatesGroup.amount)
async def add_expense_amount_check(message: types.Message):
    await message.answer('⛔️ Ошибка. Введи сумму в виде числа без знаков, к примеру 2500.')


@dp.message_handler(regexp=r"\d", state=AddExpenseStatesGroup.amount)
async def add_expense_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await db.add_expense_operation(message.from_user.id, state)
    await message.answer('✅ Покупка успешно добавлена!', reply_markup=mainKeyboard)
    await state.finish()





