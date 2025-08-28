import os
import requests
from telegram.ext import Updater, MessageHandler, Filters

# Get API keys from environment variables
GEMINI_API_KEY = os.environ.get("AIzaSyC2Ne4zI8TVA3trTrOauVNmOVNYuxD2jnE")
TELEGRAM_BOT_TOKEN = os.environ.get("7986850540:AAGgI3eqUbOW840sQbyXvwEQwhumnN8iVP8")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

user_histories = {}

def ask_gemini(prompt, history=[]):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    contents = []
    for i, msg in enumerate(history):
        role = "user" if i % 2 == 0 else "model"
        contents.append({"role": role, "parts": [{"text": msg}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})
    data = {"contents": contents}
    response = requests.post(GEMINI_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        reply = response.json()
        return reply["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

def handle_message(update, context):
    user_id = update.message.chat_id
    user_text = update.message.text
    if user_id not in user_histories:
        user_histories[user_id] = []
    response = ask_gemini(user_text, user_histories[user_id])
    user_histories[user_id].append(user_text)
    user_histories[user_id].append(response)
    update.message.reply_text(response)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    print("🤖 Bot is running on Railway...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
