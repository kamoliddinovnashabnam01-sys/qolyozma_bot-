import io
import logging
import os

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from renderer import render_handwriting

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

WELCOME = (
    "Salom! 👋 Men qo'lyozma botiman.\n\n"
    "Menga istalgan matn yuboring — uni qo'lyozma uslubidagi "
    "rasmga aylantirib beraman. ✍️\n\n"
    "Buyruqlar:\n"
    "/start — botni ishga tushirish\n"
    "/help — yordam\n"
    "/bold — qalin shriftga o'tish/o'chirish"
)

HELP = (
    "📌 Qanday ishlaydi:\n"
    "1. Menga oddiy matn yuboring (masalan: 'Salom dunyo!')\n"
    "2. Men uni qo'lyozma uslubidagi rasmga aylantiraman\n\n"
    "Buyruqlar:\n"
    "/bold — qalin/oddiy shriftni almashtirish\n"
    "/start — botni qayta ishga tushirish\n\n"
    "⚠️ Bir xabarda maksimal 1500 belgi. Lotin alifbosida yozing."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP)


async def toggle_bold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.setdefault("bold", False)
    context.user_data["bold"] = not state
    holat = "qalin" if not state else "oddiy"
    await update.message.reply_text(f"Shrift endi {holat} bo'ladi. ✍️")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    bold = context.user_data.get("bold", False)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO
    )
    try:
        img = render_handwriting(text, bold=bold)
    except ValueError as exc:
        await update.message.reply_text(f"⚠️ {exc}")
        return
    except Exception:
        logger.exception("Render xatosi")
        await update.message.reply_text("⚠️ Kechirasiz, xatolik yuz berdi.")
        return

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    await update.message.reply_photo(photo=buf, caption="✍️ Qo'lyozmangiz tayyor!")


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise SystemExit("BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("bold", toggle_bold))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
