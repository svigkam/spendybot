import collections
from datetime import datetime
from enum import Enum


class Category(Enum):
    TRANSPORT = '🚌 Транспорт'
    HOUSE = '🏠 Дом'
    HEALTH = '💊 Здоровье'
    PERSONAL = '🏝 Личные расходы'
    CLOTH = '🧣 Одежда'
    NUTRITION = '🍱 Питание'
    PRESENT = '🎁 Подарки'
    FAMILY = '🧸 Семья'
    TECHNIQUE = '⌚️ Техника'
    SERVICES = '💸 Услуги'
    SALARY = '💎 Зарплата'
    OVERWORK = '💎 Подработка'
    OTHER = '💎 Другое'

    @staticmethod
    def enum_to_list(data) -> list:
        names = []
        values = []
        for i in data:
            names.append(i.name)
            values.append(i.value)
        return [names, values]



class Operation:
    def __init__(self, id, user_id, amount, category, date: datetime):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date = date

    @staticmethod
    def from_db_to_operation(data: list) -> list:
        result = []
        for operation in data:
            temp = Operation(
                id=operation[0],
                user_id=operation[1],
                amount=operation[2],
                category=operation[4],
                date=datetime.fromtimestamp(operation[5]),
            )
            result.append(temp)
        return result

    def __str__(self) -> str:
        format_time = self.date.strftime("%Y-%m-%d %H:%M")
        return f'#{self.id} от {format_time}\n{Category[self.category].value} на сумму {self.amount}₽'
