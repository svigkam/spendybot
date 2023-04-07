CMD_START_MESSAGE = """
🚀 Привет, рад тебя видеть! <b>Я Spendy, телеграм-бот,\
который поможет тебе следить за расходами и доходами</b>\
 , я помогу составить тебе статистику твоих затрат по категориям и не только!\
 \n\n📍 А теперь напиши свой баланс, чтобы мы могли начать работу (<i>не используй\
 символы, вроде точки или запятой, просто сумма</i>):
"""


def CMD_STATS_MESSAGE(balance, user_stat) -> str:
    return f"""
<b>📄 Твоя статистика:</b>

💰 Твой баланс: {balance} ₽

<b>За последние 31 день ты</b>:
▫️ Заработал: {user_stat[1]} ₽
▫️ Потратил: {user_stat[0]} ₽
"""


CMD_HELP_MESSAGE = """
💎 <b>Вот что я могу</b>:\n
▫️ <b>Баланс</b> - Покажу баланс
▫️ <b>Статистика</b> - Покажу статистику за месяц
▫️ <b>Профиль</b> - Покажу основные настройки аккаунта

▫️ <b>Добавить покупку</b>
▫️ <b>Добавить доход</b>
▫️ <b>Показать все расходы</b>
▫️ <b>Показать все доходы</b>
▫️ <b>Показать все расходы за этот месяц</b>
▫️ <b>Показать все доходы за этот месяц</b>
▫️ <b>Показать все операции</b>

▫️ <b>/start</b> - Команда для новых пользователей
▫️ <b>/help</b> - Помощь, список команд
▫️ <b>/cancel</b> - Отменить действие
"""
CMD_DELETE_MESSAGE = """
🙀 Ты уверен, что хочешь стереть о себе все данные без возможности возврата? \
Для подтверждения повторно введите /delete."""
CMD_DEL_PURCHASE_INSTRUCTION = """
❗️ Для удаления покупки введите:\
\n\t«Удалить покупку НОМЕР_ПОКУПКИ» \n\nК примеру «Удалить покупку 175685».
"""
