from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from dev_tools import get_abi, read_method
from security_checker import check_token_risk

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Avalanche Security & Dev Bot!")

async def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = context.args[0]
    result = check_token_risk(address)
    await update.message.reply_text(result)

async def getabi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = context.args[0]
    abi = get_abi(address)
    await update.message.reply_text(abi[:4000])  # Telegram msg limit

async def readmethod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address, method = context.args[0], context.args[1]
    result = read_method(address, method)
    await update.message.reply_text(f"Result: {result}")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check_token", check_token))
app.add_handler(CommandHandler("get_abi", getabi))
app.add_handler(CommandHandler("read_method", readmethod))

if __name__ == "__main__":
    app.run_polling()
