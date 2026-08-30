import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# 1. Φόρτωση των μεταβλητών από το αρχείο .env
load_dotenv()
BOT_TOKEN = os.getenv("HTTP_API_TOKEN")

# Έλεγχος αν διαβάστηκε σωστά το token
if not BOT_TOKEN:
    raise ValueError("⚠️ Προσοχή: Δεν βρέθηκε το HTTP_API_TOKEN στο αρχείο .env!")

# Ενεργοποίηση καταγραφής (logging) για να βλέπουμε τι γίνεται στην κονσόλα
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. Εντολή /start (Όταν ο χρήστης ξεκινάει το bot)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_message = (
        f"Γειά σου, {user_name}! ⚽\n"
        "Καλώς ήρθες στο Live Match Bot.\n\n"
        "Χρησιμοποίησε την εντολή /match για να δεις τη ζωντανή ροή."
    )
    await update.message.reply_text(welcome_message)

# 3. Εντολή /match (Το template που σχεδιάσαμε στη Φάση 2)
async def live_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ticker_text = (
        "🔴 **LIVE: Ολυμπιακός - Παναθηναϊκός** | 1-0\n"
        "-----------------------------------\n"
        "⏱️ **74'** | ⚠️ Επικίνδυνο φάουλ κερδίζει ο Ολυμπιακός έξω από την περιοχή.\n\n"
        "📊 **LIVE STATS:**\n"
        "⚽ Κατοχή: 52% - 48%\n"
        "🎯 Σουτ (Εντός): 4(2) - 3(1)\n"
        "🚩 Κόρνερ: 3 - 2\n\n"
        "_Powered by Main Sponsor_ ⚡"
    )
    
    await update.message.reply_text(ticker_text, parse_mode="Markdown")

if __name__ == '__main__':
    # Δημιουργία της εφαρμογής του bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Σύνδεση των εντολών με τις συναρτήσεις
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("match", live_match))
    
    print("🚀 Το Live Match Bot ξεκίνησε και ακούει...")
    
    # Εκκίνηση του bot (Polling)
    application.run_polling()