from config import TELEGRAM_TOKEN, MISTRAL_API_KEY, OPENAI_API_KEY
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import os
import openai
import time


openai.api_key = OPENAI_API_KEY

model = "gpt-3.5-turbo"


if os.path.exists("ai_messages_openai.txt"):
    os.remove("ai_messages_openai.txt")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("new message")
    try:
        with open('ai_messages_openai.txt', 'r') as f:
            input_message = f.read()
    except FileNotFoundError:
        with open('ai_prompt_openai.txt', 'r') as f:
            input_message = f.read()   
        with open('ai_messages_openai.txt', 'a') as f:
            f.write(input_message) 
    user_message = input_message + "\n" + update.message.text + "\n"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": user_message},
            {"role": "user", "content": f"{user_message}"}
        ]
    )

    ai_message = response['choices'][0]['message']['content'].strip()
        
    with open('ai_messages_openai.txt', 'a') as f:
        f.write("\n" + update.message.text + "\n" + ai_message)
    await update.message.reply_text(ai_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    initial_prompt = "Hello ! Nice to meet you my friend !"
    await update.message.reply_text(initial_prompt)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text(), chat))

app.run_polling()



