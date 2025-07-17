import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "7203832363:AAEDhIBN2KxOvJtSRPPqZjn5LLfkWsalK_g"
ADMIN_ID = 8083799335

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class OrderState(StatesGroup):
    name = State()
    design_type = State()
    price = State()
    content = State()

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("👋 Salom! Dizayn buyurtma botiga xush kelibsiz.\n\nIltimos, to‘liq ismingizni yozing:")
    await state.set_state(OrderState.name)

@dp.message(OrderState.name)
async def ask_design_type(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="YouTube avatarka"), KeyboardButton(text="Profil avatar")],
        [KeyboardButton(text="Logo")],
        [KeyboardButton(text="YouTube Banner")],
        [KeyboardButton(text="YouTube Prevyu")],
        [KeyboardButton(text="Outro")]
    ], resize_keyboard=True)
    await message.answer("🎨 Qanday dizayn xizmati kerak? Tanlang:", reply_markup=kb)
    await state.set_state(OrderState.design_type)

@dp.message(OrderState.design_type)
async def ask_price(message: Message, state: FSMContext):
    await state.update_data(design_type=message.text)
    await message.answer("💰 Siz xohlagan dizayn narxini yozing (so‘mda):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(OrderState.price)

@dp.message(OrderState.price)
async def ask_content(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("📝 Dizayn ichida qanday elementlar bo‘lishini istaysiz?\n(Masalan: rang, rasm, yozuv, fon...)")
    await state.set_state(OrderState.content)

@dp.message(OrderState.content)
async def finish(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    data = await state.get_data()

    msg = (
        f"🆕 *Yangi buyurtma!*\n\n"
        f"👤 Ism: {data['name']}\n"
        f"🎨 Dizayn turi: {data['design_type']}\n"
        f"💰 Narxi: {data['price']} so‘m\n"
        f"📝 Tafsilotlar: {data['content']}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")
    await message.answer("✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog‘lanamiz.")
    await state.clear()

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
