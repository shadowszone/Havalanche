from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from security_checker import check_token_risk
from dev_tools import get_abi, read_method
from defillama_tools import get_token_price

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Avalanche Security & Dev Bot!")

async def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address = context.args[0]
        result = check_token_risk(address)
        await update.message.reply_text(result)
    except IndexError:
        await update.message.reply_text("Usage: /check_token <contract_address>")

async def getabi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address = context.args[0]
        abi = get_abi(address)
        await update.message.reply_text(abi[:4000])
    except IndexError:
        await update.message.reply_text("Usage: /get_abi <contract_address>")

async def readmethod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address, method = context.args[0], context.args[1]
        result = read_method(address, method)
        await update.message.reply_text(f"Result: {result}")
    except IndexError:
        await update.message.reply_text("Usage: /read_method <contract_address> <method_name>")

async def getprice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        token = context.args[0]
        result = get_token_price(token)
        await update.message.reply_text(result)
    except IndexError:
        await update.message.reply_text("Usage: /get_price <coingecko_id>")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check_token", check_token))
app.add_handler(CommandHandler("get_abi", getabi))
app.add_handler(CommandHandler("read_method", readmethod))
app.add_handler(CommandHandler("get_price", getprice))

if __name__ == "__main__":
    app.run_polling()
