import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_URL = os.getenv("API_URL", "http://api:8000")

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚕 Safar topish"), KeyboardButton(text="🚗 Haydovchi bo‘lish")],
            [KeyboardButton(text="➕ Safar joylash"), KeyboardButton(text="📍 Lokatsiya yuborish", request_location=True)],
            [KeyboardButton(text="🧳 Safarlarim"), KeyboardButton(text="👤 Profilim")],
            [KeyboardButton(text="⭐ Sevimlilar"), KeyboardButton(text="💳 Obuna")],
            [KeyboardButton(text="📞 Yordam")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo‘limni tanlang",
    )

async def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN .env faylida ko‘rsatilishi kerak")
    bot = Bot(TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "Assalomu alaykum! 🚙\\nViloyatga Boramiz — Manzilingiz bir, yo‘lingiz bir.",
            reply_markup=main_keyboard(),
        )

    @dp.message(F.location)
    async def location(message: Message):
        loc = message.location
        await message.answer(f"Lokatsiya qabul qilindi: {loc.latitude:.5f}, {loc.longitude:.5f}")

    @dp.message(F.text == "🚕 Safar topish")
    async def find_trip(message: Message):
        await message.answer(
            f"Safar qidirish uchun veb-ilovadan foydalaning: {os.getenv('WEB_ORIGIN', 'http://localhost:3000')}\\n"
            "Botdagi to‘liq qidiruv oqimi keyingi bosqichda API bilan ulanadi."
        )

    @dp.message(F.text == "📞 Yordam")
    async def help_message(message: Message):
        await message.answer("Yordam uchun administrator bilan bog‘laning. Aloqa manzili administrator sozlamalarida belgilanadi.")

    @dp.message()
    async def fallback(message: Message):
        await message.answer("Iltimos, menyudagi tugmalardan birini tanlang.", reply_markup=main_keyboard())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
