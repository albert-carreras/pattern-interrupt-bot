# Pattern Interrupt Bot

A Telegram bot that sends random pattern interrupt reminders during your wake hours.

## Setup

1. Create a new Telegram bot:
    - Message @BotFather on Telegram
    - Use the /newbot command
    - Follow the prompts to create your bot
    - Save the API token you receive

2. Get your Chat ID:
    - Message your new bot
    - Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
    - Look for the "chat":{"id":XXXXXXXXX} value

3. Set up the environment:
   ```bash
   # Clone the repository
   git clone <your-repo-url>
   cd pattern-interrupt-bot

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your actual tokens
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

5. Start the bot:
    - Message your bot with /start
    - You'll receive 3 random check-ins during your wake hours

## Configuration

- Adjust wake and sleep times in `config.py`
- Modify check-in messages in `main.py`

## Deployment

You can deploy this bot for free on:

- GitHub Actions (with scheduled runs)
- Railway.app (free tier)
- Fly.io (free tier)
- Python Anywhere (free tier)

## Security Note

Never commit your `.env` file or share your bot token publicly.