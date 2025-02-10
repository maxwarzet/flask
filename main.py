import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your actual keys
TELEGRAM_BOT_TOKEN = "7481793222:AAHzLRvIHvq0ZvuJ1xRBIO72lE-12WelBGY"
DEEPSEEK_API_KEY = "sk-d229ae67022b48f68ef56ca7ca9fc7a5"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/generate"  # Replace with actual API endpoint

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a message, and I'll respond using DeepSeek AI.")

async def chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = query_deepseek(user_message)
    await update.message.reply_text(response)

def query_deepseek(prompt):
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {"prompt": prompt, "max_tokens": 200}
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("text", "Sorry, I couldn't generate a response.")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
