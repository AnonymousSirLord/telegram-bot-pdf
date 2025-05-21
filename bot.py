import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from parser import extract_text_from_pdf, parse_rate_info

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Send me a PDF rate confirmation to extract data.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"temp/{update.message.document.file_unique_id}.pdf"
    os.makedirs("temp", exist_ok=True)
    await file.download_to_drive(file_path)

    raw_text = extract_text_from_pdf(file_path)
    data = parse_rate_info(raw_text)

    response = "📋 *Extracted Info:*\n"
    for key, values in data.items():
        if values:
            response += f"*{key}:* {values[0]}\n"
        else:
            response += f"*{key}:* Not found\n"

    await update.message.reply_markdown(response)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_document))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
