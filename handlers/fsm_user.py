from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.bot_db import get_qr_code, get_category, get_guide, insert_sql, get_qr_code_tour, get_username_user
from keyboards.client_kb import (
    submit_markup,
    cancel_markup,
    quantity_markup
)


class FSMAdmin(StatesGroup):
    qr_code = State()
    username = State()
    quantity = State()
    number = State()
    submit = State()


async def fsm_start(message: types.Message):
    await FSMAdmin.qr_code.set()
    await message.answer("Введите код тура: ")


async def load_qr_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["qr_code"] = await get_qr_code_tour(message.text)
    tour = await get_qr_code(message.text)
    category = await get_category(tour[13])
    guide = await get_guide(tour[14])
    site = f"<a href='http://164.92.190.147:8880/home/tour/{tour[4]}'>Tour</a>"
    await message.answer(
        f"\nТур: <i>{tour[1]}</i>"
        f"\nЦена: <i>{tour[3]}</i>"
        f"\nДата выезда: <i>{tour[6]}</i>"
        f"\nДата приезда: <i>{tour[7]}</i>"
        f"\nЛимит: <i>{tour[8]}</i>"
        f"\nСколько: <i>{tour[9]}</i>"
        f"\nДлительность: <i>{tour[11]} дней</i>"
        f"\nСложность: <i>{tour[12]}</i>"
        f"\nГид: <i>{guide[0]} {guide[1]}</i>"
        f"\nКатегория: <i>{category[0]}</i>"
        f"\nSite: <i>{site}</i>",
        parse_mode="HTML",
    )
    await FSMAdmin.next()
    await message.answer(
        "Если хотите этот тур забронировать то тогда \nВведите ваш username (Которого ввели при регистраций")
    await message.answer("Если не этот тур то тогда нажмите на Cancel", reply_markup=cancel_markup)


async def load_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = await get_username_user(message.text)
    await FSMAdmin.next()
    await message.answer(
        "Сколько мест хотите забронировать", reply_markup=quantity_markup
    )


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["quantity"] = message.text
    await FSMAdmin.next()
    await message.answer("Введите номер телефона:", reply_markup=cancel_markup)


async def load_number(message: types.Message, state: FSMContext):
    if (
            int(message.text)
            and len(str(message.text)) == 10
            and str(message.text).startswith("0")
    ):
        async with state.proxy() as data:
            data["number"] = f"+996{message.text}"
        await message.answer(
            f'\nUsername: {data["username"]}'
            f'\nНомер: {data["number"]} '
            f'\nКоличество: {data["quantity"]}'
            f'\nКод Тура: {data["qr_code"]}'
        )
        await FSMAdmin.next()
        await message.answer("Все данные правильны?", reply_markup=submit_markup)

    else:
        await message.answer(
            "Введите номер: например 0777123456", reply_markup=cancel_markup
        )


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await insert_sql(state)
        await state.finish()
        await message.answer(
            "Бронь успешно завершена"
            "\n<i><b>В скором времени с вами свяжется Гид.</b></i>"
            "\n<b> Хорошего дня!</b>🤗 ",
            parse_mode="HTML",
        )
    elif message.text == ["НЕТ", "CANCEL"]:
        await message.answer(
            "Отмена! Чтобы заново пройти регистрацию нажмите на команду /reg"
        )
        await state.finish()
    else:
        await message.answer("ДА или НЕТ?!")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer("Вы отменили бронь! Чтобы начать заново нажмите на /arrange")
        await state.finish()


def register_handlers_fsm_student(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=["CANCEL"])
    dp.register_message_handler(
        cancel_reg, Text(equals=["CANCEL", "Отмена"], ignore_case=True), state=["*"]
    )
    dp.register_message_handler(fsm_start, commands=["arrange"])
    dp.register_message_handler(load_qr_code, state=FSMAdmin.qr_code)
    dp.register_message_handler(load_username, state=FSMAdmin.username)
    dp.register_message_handler(load_number, state=FSMAdmin.number)
    dp.register_message_handler(load_quantity, state=FSMAdmin.quantity)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
