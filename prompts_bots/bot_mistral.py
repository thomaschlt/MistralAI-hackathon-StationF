from config import TELEGRAM_TOKEN, MISTRAL_API_KEY
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

model = "mistral-large-latest"
client = MistralClient(api_key=MISTRAL_API_KEY)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("new message")
    try:
        with open('ai_messages.txt', 'r') as f:
            input_message = f.read()
    except FileNotFoundError:
        with open('ai_prompt.txt', 'r') as f:
            input_message = f.read()    
    user_message = input_message + "\n" + update.message.text + "\n"
    chat_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=user_message)]
    )
    ai_message = chat_response.choices[0].message.content
    with open('ai_messages.txt', 'a') as f:
        f.write(user_message + "\n" + ai_message + '\n')
    await update.message.reply_text(ai_message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    initial_prompt = "Hello ! Nice to meet you my friend !"
    await update.message.reply_text(initial_prompt)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text(), chat))

app.run_polling()



