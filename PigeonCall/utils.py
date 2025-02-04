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
    If the AI also includes the tweet ID, it should be formatted as {{TWEET_ID:123456789}}.

    Args:
        raw_output (str): The raw AI-generated response.

    Returns:
        str: The extracted tweet text.
    """
    start_marker, end_marker = "{{TWEET_START}}", "{{TWEET_END}}"
    start_idx, end_idx = raw_output.find(start_marker), raw_output.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        return raw_output[start_idx + len(start_marker):end_idx].strip()
    
    return raw_output.strip()  # Fallback if markers aren't found

# extracts info from prompt for together AI
def extract_tweet_and_id(raw_output: str) -> tuple:
    """
    Extracts tweet text, tweet ID, and username from AI-generated response.

    Assumes GrokAI provides a response with:
    - `Tweet: <tweet content>`
    - `ID: <tweet ID>`
    - `Username: @<handle>`
    - `Context: <brief context>`

    Returns:
        - tweet_text (str): The extracted tweet content.
        - tweet_id (str | None): Extracted tweet ID, or None if missing.
        - username (str | None): Extracted username (Twitter handle), or None if missing.
        - context (str | None): Brief context for the tweet, or None if missing.

    """
 # Regex patterns to extract each part
    tweet_pattern = r"Tweet:\s*\"(.*?)\""
    id_pattern = r"ID:\s*(\d+)"
    username_pattern = r"Username:\s*(@\w+)"
    context_pattern = r"Context:\s*(.*)"

    # Extract values using regex
    tweet_match = re.search(tweet_pattern, raw_output)
    id_match = re.search(id_pattern, raw_output)
    username_match = re.search(username_pattern, raw_output)
    context_match = re.search(context_pattern, raw_output)

    # Extracted values (default to None if not found)
    tweet_text = tweet_match.group(1).strip() if tweet_match else None
    tweet_id = id_match.group(1).strip() if id_match else None
    username = username_match.group(1).strip() if username_match else None
    context = context_match.group(1).strip() if context_match else None

    return tweet_text, tweet_id, username, context
