import logging
import math
from datetime import datetime

from aiogram.dispatcher import FSMContext

from database import sqlite_db as db
from models.operation_model import Operation
from models.user_model import User


async def init() -> None:
    await db.db_connect()


def create_pagination(data: list) -> list:
    result = []
    items_on_one_page = 5
    pages = math.ceil(len(data) / items_on_one_page)
    for i in range(pages):
        temp = []
        for k in range(items_on_one_page):
            index = i * items_on_one_page + k
            if index < len(data):
                temp.append(data[index])
        result.append(temp)
    return result


# USER WORK


async def add_user(user_id: int, state: FSMContext) -> None:
    notice_toggle = True
    async with state.proxy() as data:
        await db.add_user(user_id=int(user_id), balance=float(data['balance']), notifications=notice_toggle)


async def get_user(user_id: int) -> User:
    request_data = await db.get_user(int(user_id))
    return User.from_db_to_user(request_data)


async def user_is_exist(user_id: int) -> bool:
    request_data = await db.get_user(int(user_id))
    return request_data is not None


async def update_user(user_id: int, balance: float, notice: bool):
    await db.update_user(user_id, balance, notice)


async def update_user_balance(user_id: int, balance: float):
    user = await get_user(user_id)
    await db.update_user(user_id, balance, user.notice)


async def update_user_notice(user_id: int):
    user = await get_user(user_id)
    new_notice = not user.notice
    await db.update_user(user_id, user.balance, new_notice)


async def auto_update_user_balance(user_id: int, amount: float):
    user = await get_user(user_id)
    current_balance = user.balance + amount
    logging.info(f'Баланс: {user.balance}, изменение на: {amount}. Новое значение баланса: {current_balance}')
    await update_user(user_id, current_balance, user.notice)


async def delete_user(user_id: int) -> None:
    await db.delete_userdata(user_id)


# OPERATION ADD WORK


async def add_expense_operation(user_id: int, state: FSMContext) -> None:
    date = datetime.timestamp(datetime.now())
    async with state.proxy() as data:
        await db.add_operation(user_id, float(data['amount']), 'Expense', data['category'], date)
        await auto_update_user_balance(user_id, -float(data['amount']))


async def add_income_operation(user_id: int, state: FSMContext) -> None:
    date = datetime.timestamp(datetime.now())
    async with state.proxy() as data:
        await db.add_operation(user_id, float(data['amount']), 'Income', data['category'], date)
        await auto_update_user_balance(user_id, float(data['amount']))

# OPERATION GET WORK


async def get_all_operations(user_id: int) -> list[[Operation]]:
    request_data = await db.get_all_operations(user_id)
    return create_pagination(Operation.from_db_to_operation(request_data))


async def get_all_income_operations(user_id: int, period: int) -> list[Operation]:
    format_period = datetime.timestamp(datetime.now()) - period
    request_data = await db.get_all_operations_from_type_and_period(user_id, 'Income', format_period)
    return Operation.from_db_to_operation(request_data)


async def get_all_expense_operations(user_id: int, period: int) -> list[Operation]:
    format_period = datetime.timestamp(datetime.now()) - period
    request_data = await db.get_all_operations_from_type_and_period(user_id, 'Expense', format_period)
    return Operation.from_db_to_operation(request_data)


async def delete_operation_by_id(user_id: int, id: int):
    await db.delete_operation_by_id(user_id, id)
