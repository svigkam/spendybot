from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove

from models.operation_model import Category

startKeyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('/start')]], resize_keyboard=True)

cancelKeyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('/cancel')]], resize_keyboard=True)


def get_paginationKeyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('←', callback_data='pageback'), InlineKeyboardButton('→', callback_data='pagenext')],
        [InlineKeyboardButton('Закрыть список', callback_data='pageclose')],
        [InlineKeyboardButton('Как удалить операцию❔', callback_data='pagedelete')],
    ])


def get_profileKeyboard(notice: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f'Авторассылка: {"Вкл" if notice else "Выкл"}', callback_data='notice_toggle')],
        [InlineKeyboardButton('Изменить баланс', callback_data='set_balance')],
        [InlineKeyboardButton('Удалить аккаунт', callback_data='delete_user')],
    ])


statsKeyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Показать историю')],
    [KeyboardButton('Расходы'), KeyboardButton('Доходы')],
    [KeyboardButton('Назад'), KeyboardButton('Совет')]
], resize_keyboard=True)

mainKeyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Баланс')],
    [KeyboardButton('Добавить доход'), KeyboardButton('Добавить покупку')],
    [KeyboardButton('Статистика'), KeyboardButton('Профиль')],
], resize_keyboard=True)

addIncomeKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Зарплата', callback_data='SALARY'),
     InlineKeyboardButton('Подарок', callback_data='PRESENT')],
    [InlineKeyboardButton('Подработка', callback_data='OVERWORK'),
     InlineKeyboardButton('Другое', callback_data='OTHER')],
], resize_keyboard=True)

expens_cat = Category.enum_to_list(Category)

addExpenseKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(expens_cat[1][0], callback_data=expens_cat[0][0]),
     InlineKeyboardButton(expens_cat[1][1], callback_data=expens_cat[0][1]),
     InlineKeyboardButton(expens_cat[1][2], callback_data=expens_cat[0][2])],
    [InlineKeyboardButton(expens_cat[1][3], callback_data=expens_cat[0][3]),
     InlineKeyboardButton(expens_cat[1][4], callback_data=expens_cat[0][4]),
     InlineKeyboardButton(expens_cat[1][5], callback_data=expens_cat[0][5])],
    [InlineKeyboardButton(expens_cat[1][6], callback_data=expens_cat[0][6]),
     InlineKeyboardButton(expens_cat[1][7], callback_data=expens_cat[0][7]),
     InlineKeyboardButton(expens_cat[1][8], callback_data=expens_cat[0][8])],
], resize_keyboard=True)
