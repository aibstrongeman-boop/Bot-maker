from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

# ضع توكن البوت الذي سيحوّل الملفات
TOKEN = "8343139529:AAEAb4xFox4ETK1hpQMdonsG0PfQQrh0btY"

# استقبال ملفات بايثون
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.endswith(".py"):
        await update.message.reply_text("❌ فقط ملفات Python (.py) مسموحة")
        return

    file_id = document.file_id
    file_name = document.file_name

    # تحميل الملف مؤقتاً
    file_path = await document.get_file()
    await file_path.download_to_drive(file_name)

    # إنشاء كود البوت الجديد (متقدم)
    bot_code = f'''
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ضع هنا توكن البوت الجديد بعد إنشاءه من BotFather
TOKEN = "PUT_YOUR_NEW_BOT_TOKEN_HERE"

# كيبورد أساسي
reply_keyboard = [
    [KeyboardButton("🔹 خيار 1"), KeyboardButton("🔹 خيار 2")],
    [KeyboardButton("🔹 خيار 3")]
]

# كيبورد داخلي
inline_keyboard = [
    [InlineKeyboardButton("✅ زر 1", callback_data="btn1")],
    [InlineKeyboardButton("✅ زر 2", callback_data="btn2")],
    [InlineKeyboardButton("✅ زر 3", callback_data="btn3")]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بك! اختر زر من الكيبورد:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in ["🔹 خيار 1", "🔹 خيار 2", "🔹 خيار 3"]:
        await update.message.reply_text("اختر زر من الانلاين:", reply_markup=InlineKeyboardMarkup(inline_keyboard))
    else:
        await update.message.reply_text(f"لقد ضغطت: {{text}}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(f"تم الضغط على: {{query.data}}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
'''

    # حفظ الملف النهائي للبوت
    new_file_name = f"bot_from_{file_name}"
    with open(new_file_name, "w", encoding="utf-8") as f:
        f.write(bot_code)

    # إرسال الملف النهائي للمستخدم
    await update.message.reply_document(document=open(new_file_name, "rb"))
    await update.message.reply_text("✅ تم إنشاء البوت بنجاح! عدّل توكن البوت الجديد قبل التشغيل.")

# تشغيل البوت المحول
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.FileExtension("py"), handle_file))
app.run_polling()