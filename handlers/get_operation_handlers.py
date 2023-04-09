from aiogram import types

from repositories import db_repo as db
from keyboards import get_paginationKeyboard
from main import dp

page_number = 0
max_pages = 1


async def get_operations_from_repo(user_id: int) -> str:
    global max_pages
    data = await db.get_all_operations(user_id)
    max_pages = len(data) - 1
    page_data = data[page_number]
    post = f'🗃 <b>Операции. Страница номер {page_number + 1}</b>.\n\n'
    for operation in page_data:
        post += operation.__str__() + '\n\n'
    return post


@dp.message_handler(text='Показать историю')
async def show_all_operations(message: types.Message):
    post = await get_operations_from_repo(message.from_user.id)
    await message.delete()
    await message.answer(post, parse_mode='HTML', reply_markup=get_paginationKeyboard())


@dp.callback_query_handler(lambda cb: cb.data.startswith('page'))
async def page_callback_handler(callback: types.CallbackQuery):
    global page_number
    if callback.data.endswith('close'):
        return await callback.message.delete()
    elif callback.data.endswith('delete'):
        return await callback.answer('❕ Для удалении покупки/дохода напиши мне "Удалить операцию"')
    elif page_number == max_pages and callback.data.endswith('next') or page_number == 0 and callback.data.endswith(
            'back'):
        return await callback.answer('❌ Это невозможно!')
    elif callback.data.endswith('next') and page_number < max_pages:
        page_number += 1
    elif callback.data.endswith('back') and page_number > 0:
        page_number -= 1
    post = await get_operations_from_repo(callback.from_user.id)
    await callback.message.edit_text(post, parse_mode='HTML', reply_markup=get_paginationKeyboard())
    await callback.answer(' ')


# ========================= DELETE OPERATION =========================


@dp.message_handler(text='Удалить операцию')
async def cmd_delete_operation(message: types.Message):
    await message.answer('Для удаления покупки введите "Удалить операцию НОМЕР_ОПЕРАЦИИ". '
                         'К примеру "Удалить операцию 175685" ', parse_mode='HTML')


@dp.message_handler(lambda message: message.text.startswith('Удалить операцию '))
async def cmd_delete_operation(message: types.Message):
    query = message.text[17:]
    await db.delete_operation_by_id(message.from_user.id, query)
    await message.answer('😊 Если такова и существовала, то её больше нет!', parse_mode='HTML')
