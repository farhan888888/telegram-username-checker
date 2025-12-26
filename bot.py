from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.error import BadRequest
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    lines = update.message.text.splitlines()
    valid = []

    for line in lines:
        username = line.strip()
        if not username:
            continue

        if not username.startswith("@"):
            username = "@" + username

        try:
            await context.bot.get_chat(username)
            valid.append(username)
        except BadRequest:
            pass

    if valid:
        await update.message.reply_text("\n".join(valid))
    else:
        await update.message.reply_text("No valid usernames found.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
