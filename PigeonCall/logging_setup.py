import logging
import os
from datetime import datetime

# ====================== #
# 📝 LOGGING MANAGEMENT  #
# ====================== #

# ✅ Get the directory where bot.py is located
bot_directory = os.path.dirname(os.path.abspath(__file__))

# ✅ Ensure logs are stored inside the bot's directory
log_dir = os.path.join(bot_directory, "logs")
os.makedirs(log_dir, exist_ok=True)  # ✅ Create logs directory if it doesn’t exist

# ✅ Set the correct log file path
log_file = os.path.join(log_dir, "bot_log.txt")
file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")

# Ensure logs directory exists
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# Set up logging
log_file = os.path.join(log_dir, "bot_log.txt")

# ✅ Define handlers first
file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")  # ✅ Now writes inside logs/
console_handler = logging.StreamHandler()

# ✅ Set formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

def log_tweet_decision(context, is_reply, model, tweet_text, tweet_id=None, username=None):
    """Logs the decision to both console and a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[{timestamp}] 🔥 Tweet Decision\n"
    log_entry += f"🔄 Is Reply?: {'Yes' if is_reply else 'No'}\n"
    if is_reply:
        log_entry += f"📌 Replying to: @{username} (Tweet ID: {tweet_id})\n"
    log_entry += f"📝 Context: {context}\n"
    log_entry += f"⚙️ Generation Route: {model}\n"
    log_entry += f"📢 Final Tweet: {tweet_text}\n"
    log_entry += "=" * 50  # Separator for readability

    logging.info(log_entry)
