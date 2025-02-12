import os
import random
import datetime
import logging
from telegram.ext import Application, CommandHandler
import asyncio
from config import TELEGRAM_TOKEN, CHAT_ID, WAKE_TIME, SLEEP_TIME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PATTERN_MESSAGES = [
    "🔍 Quick Check-in:\n1. What's on your mind?\n2. Rate it: Productive (P) or Circular (C)\n3. If Circular: Change position, room, or focus for 2min",
    "⏰ Awareness Moment:\n1. Notice your current thoughts\n2. P or C?\n3. If C: Stand up, walk around, observe 3 objects",
    "🎯 Pattern Check:\n1. Current thought pattern?\n2. P/C?\n3. If C: Change your environment for 2min"
]

def get_schedule_times():
    wake_hour, wake_minute = map(int, WAKE_TIME.split(':'))
    sleep_hour, sleep_minute = map(int, SLEEP_TIME.split(':'))

    now = datetime.datetime.now()
    today_wake = now.replace(hour=wake_hour, minute=wake_minute, second=0)
    today_sleep = now.replace(hour=sleep_hour, minute=sleep_minute, second=0)

    available_minutes = (today_sleep - today_wake).seconds // 60
    if available_minutes < 3:
        available_minutes = 1
        random_minutes = [0, 0, 1]
    else:
        random_minutes = sorted(random.sample(range(available_minutes), 3))

    return [today_wake + datetime.timedelta(minutes=m) for m in random_minutes]

async def send_telegram_message(message: str):
    async with Application.builder().token(TELEGRAM_TOKEN).build() as app:
        await app.bot.send_message(chat_id=CHAT_ID, text=message)
        logger.info("Message sent successfully!")

async def schedule_messages():
    message_times = get_schedule_times()
    now = datetime.datetime.now()

    logger.info(f"Current time: {now.strftime('%H:%M:%S')}")
    logger.info(f"Wake time: {WAKE_TIME}")
    logger.info(f"Sleep time: {SLEEP_TIME}")
    logger.info("Scheduled message times:")

    for i, message_time in enumerate(message_times, 1):
        logger.info(f"Message {i}: {message_time.strftime('%H:%M:%S')}")

    for message_time in message_times:
        delay = (message_time - now).total_seconds()
        if delay > 0:
            logger.info(f"Waiting {delay:.2f} seconds until next message...")
            await asyncio.sleep(delay)
            await send_telegram_message(random.choice(PATTERN_MESSAGES))

async def start(update, context):
    logger.info("Bot received /start command")
    await update.message.reply_text(
        "Pattern Interrupt Bot activated! You'll receive 3 random check-ins during your wake hours."
    )
    await schedule_messages()

def main():
    logger.info("Starting Pattern Interrupt Bot...")
    logger.info(">>> Please send /start to your bot in Telegram to begin <<<")

    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        logger.info("Bot initialized successfully")
        app.run_polling()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()