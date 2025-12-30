# main.py
import ast
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BOT_TOKEN = "8343139529:AAEAb4xFox4ETK1hpQMdonsG0PfQQrh0btY"

def extract_functions(py_code: str):
    tree = ast.parse(py_code)
    funcs = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                funcs.append(node.name)
    return funcs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ارسل ملف بايثون (.py)\n"
        "راح أحوّله إلى بوت بأزرار (تعليمي/آمن)."
    )

async def handle_py(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith(".py"):
        await update.message.reply_text("❌ بس ملفات .py")
        return

    file_path = os.path.join(UPLOAD_DIR, doc.file_name)
    file = await doc.get_file()
    await file.download_to_drive(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    funcs = extract_functions(code)
    if not funcs:
        await update.message.reply_text("❌ ما لقيت دوال قابلة للتحويل.")
        return

    keyboard = [[f] for f in funcs]
    context.user_data["funcs"] = funcs

    await update.message.reply_text(
        "✅ تم التحليل. اختَر دالة:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    funcs = context.user_data.get("funcs", [])

    if text in funcs:
        await update.message.reply_text(
            f"🔹 الدالة: `{text}`\n\n"
            "🧪 هذا وضع تعليمي.\n"
            "تگدر تربطها لاحقًا بـ Wrapper آمن أو Demo output.",
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_py))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
