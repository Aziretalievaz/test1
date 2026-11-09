from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import Register
from keyboards import registration_keyboard

router = Router()
users_data = {}


@router.message(Command("start"))
async def start(message: Message):
    name = message.from_user.first_name

    await message.answer(f"Привет, {name}!")


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/register — регистрация\n"
        "/profile — мой профиль"
    )


@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)

    await message.answer("Шаг 1: Введите ваше имя:")


@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(Register.age)

    await message.answer("Шаг 2: Введите ваш возраст:")


@router.message(Register.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Это не число! Пожалуйста, введите возраст цифрами:")
        return

    age = int(message.text)

    if age <= 0:
        await message.answer("Возраст должен быть больше нуля. Попробуйте ещё раз:")
        return

    await state.update_data(age=age)

    data = await state.get_data()

    await message.answer(
    f"Проверьте ваши данные:\n"
    f"Имя: {data['name']}\n"
    f"Возраст: {data['age']}",
    reply_markup=registration_keyboard()
)

@router.callback_query(F.data == "confirm_reg")
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = callback.from_user.id

    users_data[user_id] = {
        "name": data["name"],
        "age": data["age"]
    }

    await callback.message.answer("Регистрация завершена!")
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == "restart_reg")
async def restart_registration(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await state.set_state(Register.name)

    await callback.message.answer("Начнем заново. Шаг 1: Введите ваше имя:")

    await callback.answer()


@router.message(Command("profile"))
async def profile(message: Message):
    user_id = message.from_user.id

    if user_id in users_data:
        data = users_data[user_id]

        await message.answer(
            f"Ваши данные:\n"
            f"Имя — {data['name']}\n"
            f"Возраст — {data['age']}"
        )
    else:
        await message.answer(
            "Вы не зарегистрированы. Напишите /register, чтобы пройти регистрацию."
        )