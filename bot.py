import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import openai

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)
openai.api_key = os.getenv("OPENAI_API_KEY")

@dp.message_handler()
async def handle(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in os.getenv("AUTHORIZED_USERS", "").split(","):
        await message.reply("Bạn không có quyền dùng bot này.")
        return

    res = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": message.text}]
    )
    reply = res.choices[0].message["content"]
    await message.reply(reply)

if __name__ == '__main__':
    executor.start_polling(dp)
