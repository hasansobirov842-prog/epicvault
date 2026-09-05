import os
import random
import sqlite3
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

DB = "batl.db"

QUESTIONS = [
    ("O'zbekiston poytaxti qaysi?", ["Toshkent", "Samarqand", "Buxoro", "Andijon"], 0),
    ("2 + 2 nechchi?", ["3", "4", "5", "6"], 1),
    ("Haftada nechta kun bor?", ["5", "6", "7", "8"], 2),
    ("Yerning tabiiy yo'ldoshi nima?", ["Quyosh", "Oy", "Mars", "Venera"], 1),
    ("10 × 5 nechchi?", ["40", "45", "50", "55"], 2),
    ("O'zbekiston bayrog'ida nechta rang bor?", ["3", "4", "5", "6"], 1),
    ("1 kilometr nechta metr?", ["100", "500", "1000", "10000"], 2),
    ("Eng katta okean qaysi?", ["Atlantika", "Hind", "Tinch", "Shimoliy Muz"], 2),
]

waiting_player = None
battles = {}


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    """)

    con.commit()
    con.close()


def save_user(user):
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)",
        (user.id, user.username or "")
    )
    con.commit()
    con.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user)

    keyboard = [
        [InlineKeyboardButton("⚔️ BATLGA KIRISH", callback_data="join_battle")],
        [InlineKeyboardButton("📊 Statistika", callback_data="stats")]
    ]

    await update.message.reply_text(
        "⚔️ **BATL ARENASIGA XUSH KELIBSAN!**\n\n"
        "👥 2 ta o'yinchi ulanadi.\n"
        "🧠 Savollarga javob berasiz.\n"
        "🏆 Ko'proq to'g'ri javob bergan g'olib!\n\n"
        "Tayyor bo'lsang, batlga kir:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def join_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_player

    query = update.callback_query
    await query.answer()

    user = query.from_user
    save_user(user)

    if waiting_player == user.id:
        await query.message.reply_text("⏳ Sen allaqachon raqib kutyapsan!")
        return

    if waiting_player is None:
        waiting_player = user.id

        await query.message.reply_text(
            "⏳ **Raqib qidirilmoqda...**\n\n"
            "Boshqa o'yinchi qo'shilishi bilan batl boshlanadi.",
            parse_mode="Markdown"
        )
        return

    player1 = waiting_player
    player2 = user.id

    waiting_player = None

    battle_id = f"{player1}_{player2}"

    battles[battle_id] = {
        "players": [player1, player2],
        "scores": {
            player1: 0,
            player2: 0
        },
        "round": 0,
        "answers": {}
    }

    context.bot_data["user_battle"] = context.bot_data.get(
        "user_battle", {}
    )

    context.bot_data["user_battle"][player1] = battle_id
    context.bot_data["user_battle"][player2] = battle_id

    await context.bot.send_message(
        player1,
        "⚔️ **RAQIB TOPILDI!**\n\n"
        "🔥 BATL BOSHLANDI!",
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        player2,
        "⚔️ **RAQIB TOPILDI!**\n\n"
        "🔥 BATL BOSHLANDI!",
        parse_mode="Markdown"
    )

    await send_question(context, battle_id)


async def send_question(context, battle_id):
    battle = battles.get(battle_id)

    if not battle:
        return

    if battle["round"] >= 5:
        await finish_battle(context, battle_id)
        return

    battle["answers"] = {}
    battle["current_question"] = random.choice(QUESTIONS)

    question, options, correct = battle["current_question"]

    keyboard = []

    for i, option in enumerate(options):
        keyboard.append([
            InlineKeyboardButton(
                option,
                callback_data=f"answer:{battle_id}:{i}"
            )
        ])

    text = (
        f"⚔️ **RAUND {battle['round'] + 1}/5**\n\n"
        f"❓ {question}\n\n"
        "Javobni tanla:"
    )

    for player in battle["players"]:
        try:
            await context.bot.send_message(
                player,
                text,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception:
            pass


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split(":")

    battle_id = data[1]
    answer_index = int(data[2])

    battle = battles.get(battle_id)

    if not battle:
        await query.message.reply_text("❌ Bu batl tugagan.")
        return

    user_id = query.from_user.id

    if user_id not in battle["players"]:
        return

    if user_id in battle["answers"]:
        await query.answer("Sen allaqachon javob berding!", show_alert=True)
        return

    battle["answers"][user_id] = answer_index

    question, options, correct = battle["current_question"]

    if answer_index == correct:
        battle["scores"][user_id] += 1

    await query.edit_message_reply_markup(reply_markup=None)

    if len(battle["answers"]) == 2:
        battle["round"] += 1

        await asyncio.sleep(1)

        await send_question(context, battle_id)


async def finish_battle(context, battle_id):
    battle = battles.get(battle_id)

    if not battle:
        return

    p1, p2 = battle["players"]

    s1 = battle["scores"][p1]
    s2 = battle["scores"][p2]

    if s1 > s2:
        winner = p1
        loser = p2
    elif s2 > s1:
        winner = p2
        loser = p1
    else:
        winner = None

    if winner:
        winner_text = f"🏆 G'OLIB: [{winner}](tg://user?id={winner})"
    else:
        winner_text = "🤝 DURRANG!"

    result = (
        "🏁 **BATL YAKUNLANDI!**\n\n"
        f"👤 O'yinchi 1: `{s1}` ball\n"
        f"👤 O'yinchi 2: `{s2}` ball\n\n"
        f"{winner_text}"
    )

    for player in battle["players"]:
        try:
            await context.bot.send_message(
                player,
                result,
                parse_mode="Markdown"
            )
        except Exception:
            pass

        context.bot_data.get("user_battle", {}).pop(player, None)

    del battles[battle_id]


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    con = sqlite3.connect(DB)
    count = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    con.close()

    await query.message.reply_text(
        f"📊 **BOT STATISTIKASI**\n\n"
        f"👥 Foydalanuvchilar: {count}\n"
        f"⚔️ Hozirgi batllar: {len(battles)}",
        parse_mode="Markdown"
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("ERROR:", context.error)


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi!")

    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(join_battle, pattern="^join_battle$")
    )
    app.add_handler(
        CallbackQueryHandler(stats, pattern="^stats$")
    )
    app.add_handler(
        CallbackQueryHandler(answer, pattern="^answer:")
    )

    app.add_error_handler(error_handler)

    print("⚔️ Batl bot ishga tushdi!")

    app.run_polling()


if __name__ == "__main__":
    main()
