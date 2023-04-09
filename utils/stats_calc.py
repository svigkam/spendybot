import random
from datetime import datetime

from models.operation_model import Operation, Category
import repositories.db_repo as db
from matplotlib import pyplot as plt

from utils.config import STATS_PERIOD


async def get_user_data_for_period(user_id: int) -> list:
    period = 86400 * STATS_PERIOD
    expenses = await db.get_all_expense_operations(user_id=user_id, period=period)
    incomes = await db.get_all_income_operations(user_id=user_id, period=period)
    return [expenses, incomes]


async def get_expenses_category_graphic(user_id: int) -> str:
    data: list[Operation] = (await get_user_data_for_period(user_id))[0]
    categories = []
    for operation in data:
        if Category[operation.category].value[2:] not in categories:
            categories.append(Category[operation.category].value[2:])

    amounts = [0 for _ in range(len(categories))]
    for operation in data:
        amounts[categories.index(Category[operation.category].value[2:])] += operation.amount
    explode = [0.1 for _ in range(len(categories))]
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', shadow=True, explode=explode,
           wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"}, rotatelabels=True)
    ax.axis("equal")

    filename = f'get_expenses_graphic_{user_id}.png'
    plt.savefig(filename)
    return filename


async def get_expenses_graphic_by_days(user_id: int) -> str:
    data: list[Operation] = (await get_user_data_for_period(user_id))[0]

    i = 0
    date = []
    amount = [0]
    for operation in data:
        if len(date) == 0:
            date.append(operation.date.strftime("%d.%m"))
        if operation.date.strftime("%d.%m") != date[i]:
            date.append(operation.date.strftime("%d.%m"))
            i += 1
            amount.append(0)
        amount[i] += int(operation.amount)

    plt.bar(date, amount)
    plt.title('Ваши расходы:')
    filename = f'get_expenses_graphic_by_days_{user_id}.png'
    plt.savefig(filename)
    return filename


async def get_incomes_graphic_by_days(user_id: int) -> str:
    data: list[Operation] = (await get_user_data_for_period(user_id))[1]

    if not data:
        return 'Error'

    i = 0
    date = []
    amount = [0]
    for operation in data:
        if len(date) == 0:
            date.append(operation.date.strftime("%d.%m"))
        if operation.date.strftime("%d.%m") != date[i]:
            date.append(operation.date.strftime("%d.%m"))
            i += 1
            amount.append(0)
        amount[i] += int(operation.amount)

    plt.bar(date, amount)
    plt.title('Ваши доходы:')
    filename = f'get_incomes_graphic_by_days_{user_id}.png'
    plt.savefig(filename)
    return filename


async def get_sum_expenses_and_incomes_for_period(user_id: int) -> list:
    expenses = 0
    incomes = 0
    data = await get_user_data_for_period(user_id)

    for i in data[0]:
        expenses += i.amount

    for i in data[1]:
        incomes += i.amount

    return [expenses, incomes]



