7883595487:AAFWw9hLgjidbzUsUVViKjZKcKU3DPNFn9Qfrom aiogram import Bot, 
Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# 🔐 Твій токен
TOKEN = "7883595487:AAFuLs0SyBLJRcsKsKhAKAHOs7fu6x49wcg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Меню з кнопками тренувань
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Вт/Чт 17:30"))
keyboard.add(KeyboardButton("Вт/Чт 19:00"))
keyboard.add(KeyboardButton("Сб 13:30"))
keyboard.add(KeyboardButton("Скасувати запис"))

# Пам’ять про записаних
registrations = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привіт! Обери тренування для запису:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["Вт/Чт 17:30", "Вт/Чт 19:00", "Сб 13:30"])
async def register_user(message: types.Message):
    user_id = message.from_user.id
    session = message.text

    if session not in registrations:
        registrations[session] = []

    if user_id in registrations[session]:
        await message.answer("Ти вже записаний на це тренування!")
    elif len(registrations[session]) < 4:
        registrations[session].append(user_id)
        await message.answer(f"Тебе записано на {session} ✅")
    else:
        await message.answer("На жаль, місць більше немає 😞")

@dp.message_handler(lambda message: message.text == "Скасувати запис")
async def cancel_registration(message: types.Message):
    user_id = message.from_user.id
    for session, users in registrations.items():
        if user_id in users:
            users.remove(user_id)
            await message.answer(f"Твій запис на {session} скасовано ❌")
            return
    await message.answer("Ти не був записаний ні на яке тренування.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
