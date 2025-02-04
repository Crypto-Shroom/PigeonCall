import logging
import os
from datetime import datetime

# ============================
# 📝 LOGGING MANAGEMENT
# ============================

# Ensure logs directory exists
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# Set up logging
log_file = os.path.join(log_dir, "bot_log.txt")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Logs to file
        logging.StreamHandler()  # Logs to console
    ]
)

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
