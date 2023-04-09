import sqlite3 as sq
import logging


async def db_connect():
    global db, cur

    db = sq.connect('new.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, balance FLOAT, notifications BOOL);")
    cur.execute("CREATE TABLE IF NOT EXISTS operations(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, "
                "amount FLOAT, operation_type TEXT, category TEXT, date TIMESTAMP)")
    db.commit()


async def user_in_the_table(user_id: int) -> bool:
    return False if cur.execute(f"SELECT * FROM users "
                                f"WHERE user_id = {user_id}").fetchone() is None else True


async def add_user(user_id, balance, notifications) -> None:
    user_in_table = await user_in_the_table(user_id)
    if user_in_table is False:
        cur.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, balance, notifications))
        logging.info(f'Пользователь  добавлен в таблицу!')
    else:
        logging.info(f'Пользователь {user_id} уже находится в таблице!')
    db.commit()


async def get_user(user_id: int) -> list:
    return cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()


async def update_user(user_id: int, balance: float, notice: bool) -> None:
    cur.execute(f"UPDATE users SET balance = {balance}, notifications = {notice} "
                f"WHERE user_id = {user_id}")
    db.commit()


async def delete_userdata(user_id: int) -> None:
    logging.info(f'Попытка удалить пользователя {user_id}')
    cur.execute(f"DELETE FROM users WHERE user_id = {user_id}")
    cur.execute(f"DELETE FROM operations WHERE user_id = {user_id}")
    db.commit()
    if await user_in_the_table(user_id) is False:
        logging.info(f'Все данные о пользователе {user_id} стёрты!')
    else:
        logging.error(f'При удалении пользователя {user_id} что-то пошло не так.')


async def add_operation(user_id: int, amount: float, operation_type: str, category: str, date) -> None:
    cur.execute(f"INSERT INTO operations(user_id, amount, operation_type, category, date) "
                f"VALUES({user_id}, {amount}, '{operation_type}', '{category}', {date})")
    db.commit()


async def get_all_operations(user_id: int) -> list:
    return cur.execute(f"SELECT * FROM operations WHERE user_id = {user_id} ORDER BY date DESC").fetchall()


async def get_all_operations_from_type_and_period(user_id: int, operation_type: str, period) -> list:
    return cur.execute(f"SELECT * FROM operations "
                       f"WHERE user_id = {user_id} and "
                       f"operation_type = '{operation_type}' and "
                       f"date > {period}").fetchall()


async def delete_operation_by_id(user_id: int, id: int):
    cur.execute(f"DELETE FROM operations WHERE user_id = {user_id} and ID = {id}")
