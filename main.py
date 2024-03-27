from aiogram import executor, Dispatcher, Bot, types
from database import create_table, reg_user, add_winner, get_dates, winner_by_date, get_username_by_id, showWinningCount
import time
from datetime import datetime

token = "7050138133:AAEgkBFFsJKmV7xtQHJRXHVJ-l1ydAgKoXU"

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def echo_bot(msg: types.Message) -> None:
    await msg.answer("Набор в бар голубая устрица !")
    create_table(abs(msg.chat.id))


@dp.message_handler(commands=["reg"])
async def echo_bot(msg: types.Message) -> None:
    if (msg.from_user.username == "prsiik"):
        await msg.answer("Так, стоп....")
        time.sleep(3)
        await msg.answer("Ой Алиса привет !")
        time.sleep(3)
        await msg.answer("Мой создатель часто втыкал когда делал меня, и всегда после того как писал тебе")
        time.sleep(3)
        await msg.answer("Как будто у него вся кровь из головы уходила куда-то в другое место....")
        time.sleep(3)
        await msg.answer("Но ладно, whatever makes him happy")
        time.sleep(3)
        await msg.answer("Он просил передать тебе кое-что...")
        time.sleep(3)
        await msg.answer("""
            ⠀⠀⠀⠀⠀⢀⠴⠚⠉⠉⠑⠦⠴⠚⠋⠉⠒⢄⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠋⠀⠀⠀⠀⠀⠀⠀⠸⣄⠀⢘⡄⢷⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣏⠀⣼⠀⠀⠀
⠀⠀⠀⠀⠈⢇⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢠⠏⠀⠀⠀
⠀⠀⠀⠀⠀⠈⢣⡳⣄⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⠢⣕⠢⢄⢀⡠⠖⠋⠀⠀⠀⠀⠀⠀
⠀⠀⣠⡴⠒⠦⣄⠀⠀⠀⠉⠉⠁⠀⠀⣀⡤⠤⢄⡀⠀⠀
⢀⡞⠁⠀⠀⠀⠈⠛⠉⠉⠉⠉⠉⠉⠲⠏⠀⠀⠀⠘⢦⠀
⢸⡇⠀⠀⠀⠀⢀⡖⢳⠀⣠⠺⡄⠀⠀⠀⠀⠀⠀⠀⢘⡆
⠀⢻⠇⠀⠀⢀⣾⣶⡏⢀⣿⣴⠇⠀⠀⠀⠀⠀⠠⢀⡾⠀
⠀⡏⢠⠖⠓⡾⢿⡿⠀⠸⣿⣿⢠⠀⠢⣄⠀⠀⠀⢻⠀⠀
⢸⠀⠈⠛⠚⠁⠀⠀⠺⠃⠈⠁⠐⠦⣴⠿⠀⠀⠀⢸⡆⠀
⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀
⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡄⠀
⠀⠈⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠁⣧⠀
⠀⠀⡯⠙⠲⣄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠖⠋⠀⠀⡟⠀
⠀⠀⢳⣤⢡⣤⠉⠛⣲⡶⠒⠲⣞⠛⢉⣀⠀⠀⠀⣼⠃⠀
⠀⠀⠀⠙⠓⠧⠴⠚⠉⠀⠀⠀⠙⢦⣀⠈⠁⣀⡴⠋⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀
Алисочка, я тебя люблю !!!
        """)
    else:
        await msg.answer(reg_user(msg.from_user.id, msg.from_user.username, abs(msg.chat.id)))


@dp.message_handler(commands=["run_game"])
async def echo_bot(msg: types.Message) -> None:
    today = datetime.now()
    winningDate = today.strftime("%Y-%m-%d")
    formatted_dates = [date.strftime('%Y-%m-%d') for date in get_dates(abs(msg.chat.id))]
    if winningDate not in formatted_dates:
        win = add_winner(abs(msg.chat.id))
        if(msg.from_user.username == "VagOnOff"):
            await msg.answer(f"Ваз щас все пофикшу, а пока выиграл @{win} !!!")
        else:
            await msg.answer(f"Поздавряем, сегодня выиграл @{win}")
    else:
        await msg.answer(f"Сегодня уже была игра ! Победил @{winner_by_date(abs(msg.chat.id), winningDate)}")


@dp.message_handler(commands=["show_table"])
async def echo_bot(msg: types.Message) -> None:
    results = showWinningCount(abs(msg.chat.id))
    formattedAnswer = """Таблица лидеров: \n"""
    placeNumber = 1
    for i in results:
        formattedAnswer = formattedAnswer + f"{placeNumber}: {get_username_by_id(i[0], abs(msg.chat.id))} - {i[1]}\n"
        placeNumber += 1
    await msg.answer(f"""{formattedAnswer}""")


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)
