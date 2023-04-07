from models.operation_model import Operation
import repositories.db_repo as db
from matplotlib import pyplot as plt

from utils.config import STATS_PERIOD


async def get_user_data_for_period(user_id: int) -> list:
    period = 86400 * STATS_PERIOD
    expenses = await db.get_all_expense_operations(user_id=user_id, period=period)
    incomes = await db.get_all_income_operations(user_id=user_id, period=period)
    return [expenses, incomes]


async def get_expenses_graphic(user_id: int) -> str:
    data: list[Operation] = (await get_user_data_for_period(user_id))[0]

    categories = []
    for i in data:
        if i.category not in categories:
            categories.append(i.category)

    amounts = [0 for _ in range(len(categories))]
    for i in data:
        amounts[categories.index(i.category)] += i.amount

    fig1, ax1 = plt.subplots()
    ax1.pie(amounts, labels=categories, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    filename = f'get_expenses_graphic_{user_id}.png'
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



