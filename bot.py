from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler, \
    CallbackContext

from gpt import *
from util import *

token = load_message("token")
gpt_token = load_message("gpt_token")


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "Главное меню бота",
        "profile": "Генерация Tinder-профиля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, "*Привет*")
        await send_text(update, context, "_Как дела_")
        await send_text(update, context, "Вы написали " + update.message.text)
        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Запустить процесс?", {
            "start": "Запустить",
            "stop": "Остановить"
        })


async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token=gpt_token)

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
