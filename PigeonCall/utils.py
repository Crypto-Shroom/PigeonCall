import logging
import random
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

# ============================ #
# 🌍 HTTP REQUEST MANAGEMENT   #
# ============================ #

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """Creates a requests session with retry logic to handle transient errors."""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# ============================= #
# 🛠 TWEET EXTRACTION UTILITIES #
# ============================= #

# Extracts final tweet content
def extract_tweet(raw_output: str) -> str:
    """Extracts the tweet content and tweet ID while ignoring AI reasoning and chain-of-thought.

    The AI is instructed to wrap the final tweet inside {{TWEET_START}} and {{TWEET_END}}.

    Args:
        raw_output (str): The raw AI-generated response.

    Returns:
        str: The extracted tweet text.
    """
    start_marker, end_marker = "{{TWEET_START}}", "{{TWEET_END}}"
    start_idx, end_idx = raw_output.find(start_marker), raw_output.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        return raw_output[start_idx + len(start_marker):end_idx].strip()
    
    logging.error("❌ AI response did not follow expected format.")
    return raw_output.strip()  # Fallback if markers aren't found

# extracts info from prompt for together AI
def extract_tweet_and_id(raw_output: str) -> tuple:
    """
    Extracts tweet text, tweet ID, and username from AI-generated response.
    
    Assumes GrokAI provides a response with:
    - `Tweet: <tweet content>`
    - `ID: <tweet ID>`
    - `Username: @<handle>`
    
    Args:
        raw_output (str): The raw AI-generated response.

    Returns:
        tuple: (tweet_text, tweet_id, username)
    """
    
    logging.info(f"📝 Raw AI Output:\n{raw_output}")  # Debugging Grok response

    # Extract tweet content
    tweet_match = re.search(r"Tweet:\s*(.+)", raw_output)
    tweet_text = tweet_match.group(1).strip() if tweet_match else None

    # Extract tweet ID (Flexible: matches ID: 12345 or TWEET_ID: 12345)
    id_match = re.search(r"(?:ID|TWEET_ID)[: ]+(\d+)", raw_output, re.IGNORECASE)
    tweet_id = id_match.group(1) if id_match else None

    # Extract username
    user_match = re.search(r"Username:\s*@?(\w+)", raw_output)
    username = user_match.group(1) if user_match else None

    # Logging to detect missing tweet IDs
    if not tweet_id:
        logging.warning("⚠️ No Tweet ID found in AI response!")

    return tweet_text, tweet_id, username
