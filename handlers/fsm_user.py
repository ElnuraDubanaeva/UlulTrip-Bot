from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.bot_db import (
    get_qr_code,
    insert_sql,
    get_qr_code_tour,
    get_username_user,
    get_username,
    get_tour_title,
    get_tour_price,
    get_actual_limit,
    get_quantity_limit,
    update_actual_limit,
)
from keyboards.client_kb import (
    submit_markup,
    cancel_markup,
    quantity_markup,
    share_number,
    payment_markup,
)


class FSMAdmin(StatesGroup):
    qr_code = State()
    username = State()
    quantity = State()
    number = State()
    way_of_payment = State()
    payment = State()
    submit = State()


async def fsm_start(message: types.Message):
    await FSMAdmin.qr_code.set()
    await message.answer("Введите код тура: ")


async def load_qr_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["qr_code"] = await get_qr_code_tour(message.text)
    tour = await get_qr_code(message.text)
    await message.answer(
        (
            f"\nТур: {tour[1]}"
            f"\nЦена: {tour[3]}"
            f"\nДата выезда: {tour[6]}"
            f"\nДата приезда: {tour[7]}"
            f"\nКоличество мест: {tour[8]}"
            f"\nСколько человек забронировал: {tour[9]}"
            f"\nДлительность: {tour[11]} дней"
        )
    )
    await FSMAdmin.next()
    await message.answer(
        "Введите ваш username (Которого ввели при регистраций)"
        "\nЕсли хотите забронировать не этот тур то тогда нажмите на Cancel",
        reply_markup=cancel_markup,
    )


async def load_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = await get_username_user(message.text)
    await FSMAdmin.next()
    await message.answer(
        "Сколько мест хотите забронировать?", reply_markup=quantity_markup
    )


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        tour = data["qr_code"]
        actual_limit = await get_actual_limit(tour)
        quantity_limit = await get_quantity_limit(tour)
        if actual_limit + int(message.text) <= quantity_limit:
            data["quantity"] = message.text
            await FSMAdmin.next()
            await message.answer("Введите номер телефона:", reply_markup=share_number)
        else:
            if quantity_limit - actual_limit != 0:
                await message.answer(
                    f"К сожелению осталось только {quantity_limit - actual_limit} мест",
                    reply_markup=quantity_markup,
                )
            await message.answer(
                f"К сожелению мест не осталось. Чтобы забронировать другой тур  нажмите на CANCEL",
                reply_markup=cancel_markup,
            )


async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["number"] = message.contact.phone_number
        await FSMAdmin.next()
        await message.answer("Выберите способ оплаты:", reply_markup=payment_markup)


async def load_way_of_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        price = await get_tour_price(str(data["qr_code"][0]))
        summ = int(data["quantity"]) * int(price)
    if message.text == "MBank":
        await message.answer(f"Номер Мбанк: 0778116934 \nСумма к оплате: {summ}")
    if message.text == "Optima":
        await message.answer(f"Номер Optima: 0778116934 \nСумма к оплате: {summ}")
    async with state.proxy() as data:
        data["way_of_payment"] = message.text
        await FSMAdmin.next()
        await message.answer("Отправьте скриншот чека чтобы завершить бронь")


async def load_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["payment"] = message.photo[0].file_id
    username = await get_username(str(data["username"][0]))
    tour = await get_tour_title(str(data["qr_code"][0]))
    await message.answer_photo(
        photo=data["payment"],
        caption=f"\nUsername: {username[0]}"
                f'\nНомер: {data["number"]} '
                f'\nКоличество: {data["quantity"]}'
                f"\nТур: {tour[0]}",
    )
    await FSMAdmin.next()
    await message.answer("Все данные правильны?", reply_markup=submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await insert_sql(state)
        async with state.proxy() as data:
            tour = data["qr_code"]
            quantity = data["quantity"]
            actual_limit = await get_actual_limit(tour)
            summ = int(quantity) + actual_limit
            await update_actual_limit(tour_id=tour, quantity=summ)
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
        await message.answer(
            "Вы отменили бронь! Чтобы начать заново нажмите на /arrange"
        )
        await state.finish()


def register_handlers_fsm_student(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=["CANCEL"])
    dp.register_message_handler(
        cancel_reg, Text(equals=["CANCEL", "Отмена"], ignore_case=True), state=["*"]
    )
    dp.register_message_handler(fsm_start, commands=["arrange"])
    dp.register_message_handler(load_qr_code, state=FSMAdmin.qr_code)
    dp.register_message_handler(load_username, state=FSMAdmin.username)
    dp.register_message_handler(
        load_number, state=FSMAdmin.number, content_types=types.ContentType.CONTACT
    )
    dp.register_message_handler(load_quantity, state=FSMAdmin.quantity)
    dp.register_message_handler(load_way_of_payment, state=FSMAdmin.way_of_payment)
    dp.register_message_handler(
        load_payment, state=FSMAdmin.payment, content_types=["photo"]
    )
    dp.register_message_handler(submit, state=FSMAdmin.submit)
