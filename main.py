import asyncio
import aiogram.methods.get_chat_member as get_chat_member
from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command

from database import create_table, reg_user, add_winner, winner_by_date, \
    show_winning_count, get_result_today, check_chat_db, select_winner
from datetime import datetime

token = "7050138133:AAEgkBFFsJKmV7xtQHJRXHVJ-l1ydAgKoXU"

dp = Dispatcher()
bot = Bot(token)


async def get_username(chat_id, user_id):
    member = await bot(get_chat_member.GetChatMember(chat_id=chat_id, user_id=user_id))
    return member.user.username


@dp.message(Command("start"))
async def command_start_handler(msg: types.Message) -> None:
    if check_chat_db(abs(msg.chat.id)):
        await msg.answer("Чат уже инициализирован !")
    else:
        await msg.answer("Чат инициализирован !")
        create_table(abs(msg.chat.id))


@dp.message(Command("reg"))
async def echo_bot(msg: types.Message) -> None:
    await msg.answer(reg_user(msg.from_user.id, abs(msg.chat.id)))


@dp.message(Command("run_game"))
async def echo_bot(msg: types.Message) -> None:
    today = datetime.now()
    winningDate = today.strftime("%Y-%m-%d")
    results_today = get_result_today(abs(msg.chat.id))
    if results_today.size == 0:
        winnerId = select_winner(abs(msg.chat.id))
        winnerUsername = await get_username(msg.chat.id, winnerId)
        add_winner(abs(msg.chat.id), winnerId)
        await msg.answer(f"Поздравляем, сегодня выиграл @{winnerUsername}")
    else:
        winnerUsername = await get_username(msg.chat.id, winner_by_date(abs(msg.chat.id), winningDate))
        await msg.answer(f"Сегодня уже была игра ! Победил @{winnerUsername}")


@dp.message(Command("show_table"))
async def echo_bot(msg: types.Message) -> None:
    results = show_winning_count(abs(msg.chat.id))
    formattedAnswer = """Таблица лидеров: \n"""
    placeNumber = 1
    for i in results:
        formattedAnswer = formattedAnswer + f"{placeNumber}: {await get_username(msg.chat.id, i[0])} - {i[1]}\n"
        placeNumber += 1
    await msg.answer(f"""{formattedAnswer}""")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
