from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from security_checker import check_token_risk
from dev_tools import get_abi, read_method
from defillama_tools import get_token_price

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Havalanche Security & Dev Bot!\nUse /help to see available commands.")

# ✅ /help command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📘 Available Commands:\n"
        "/check_token <contract_address> — Analyze contract for security risks\n"
        "/get_abi <contract_address> — Fetch and display the verified ABI\n"
        "/read_method <contract_address> <method_name> — Call a view method\n"
        "/get_price <coingecko_id> — Get real-time price from DeFiLlama\n"
    )
    await update.message.reply_text(help_text)

# ✅ /check_token command
async def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address = context.args[0]
        result = check_token_risk(address)
        await update.message.reply_text(result)
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /check_token <contract_address>")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ✅ /get_abi command
async def getabi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address = context.args[0]
        abi = get_abi(address)
        if abi:
            trimmed = abi[:4000]  # Telegram max char per message is ~4096
            await update.message.reply_text(trimmed)
        else:
            await update.message.reply_text("⚠️ ABI not found or contract not verified.")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /get_abi <contract_address>")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ✅ /read_method command
async def readmethod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address, method = context.args[0], context.args[1]
        result = read_method(address, method)
        await update.message.reply_text(f"🧪 Result: {result}")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /read_method <contract_address> <method_name>")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ✅ /get_price command
async def getprice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        token = context.args[0]
        result = get_token_price(token)
        await update.message.reply_text(f"💰 {token} price: {result}")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /get_price <coingecko_id>")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ✅ Application setup
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# ✅ Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("check_token", check_token))
app.add_handler(CommandHandler("get_abi", getabi))
app.add_handler(CommandHandler("read_method", readmethod))
app.add_handler(CommandHandler("get_price", getprice))

# ✅ Run bot
if __name__ == "__main__":
    app.run_polling()
