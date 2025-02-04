# ============================ #
# 🤖 AI API REQUESTS           #
# ============================ #
import json
import random
import requests
import logging
from utils import extract_tweet_and_id, extract_tweet
from utils import requests_retry_session

# ============================ #
# 🤖 Grok API REQUESTS         #
# ============================ #

# Calls Grok to find a topic or tweet to reply to
def grok_request(api_key: str, prompt: str, timeout: int = 15) -> str:
    """Calls GrokAI for finding tweets to reply to or trending topics."""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "grok-2-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    session = requests_retry_session()
    try:
        response = session.post(url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logging.error("GrokAI request error: %s", e)
        return ""

# Function to find a tweet or topic to reply to
def find_tweet_or_topic(grok_api_key: str) -> tuple:
    """Finds a tweet to reply to or a trending topic.
    
    Returns:
        - tweet_text (str): The tweet to reply to OR the trending topic.
        - tweet_id (str | None): The ID of the tweet if it's a reply, else None.
        - username (str | None): The Twitter handle of the user if it's a reply, else None.
        - context (str | None): Additional context for the tweet, if provided by AI.
        - is_reply (bool): Whether this is a reply.
    """
    if random.random() < 0.8:
        prompt = (
#!            "Find a controversial tweet [TOPIC] worth replying to. "  # ADD YOUR THEME HERE
            "Return the tweet text, tweet ID, and the username of the author, and context or background of the tweet, formatted as:\n"
            "Tweet: <actual tweet content>\n"
            "ID: <tweet ID>\n"
            "Username: @<username>\n"
            "Context: <brief context>\n"
            "Do NOT add extra reasoning or explanation."
        )
        response = grok_request(grok_api_key, prompt)

 # Extract text, ID, username, and context
        extracted_data = extract_tweet_and_id(response)

        if len(extracted_data) == 4:
            tweet_text, tweet_id, username, context = extracted_data
            return tweet_text, tweet_id, username, context, True  # Reply case

        logging.error("❌ Unexpected response format from GrokAI: %s", response)
        return None, None, None, None, False  # Ensure correct return values

    else:  # Find a general topic
  #      prompt = "Find a trending topic in [TOPIC] and explain why it's trending."
        response = grok_request(grok_api_key, prompt)

        # Expecting response to contain topic + context (split by newline)
        topic_parts = response.split("\n", 1)
        topic_text = topic_parts[0].strip()
        context = topic_parts[1].strip() if len(topic_parts) > 1 else None

        return topic_text, None, None, context, False  # Non-reply case


# ============================ #
# ✨ AI Tweet Generation       #
# ============================ #

def together_ai_generate(api_key: str, context: str, is_reply: bool, tweet_context: str = None, username: str = None, timeout: int = 15) -> str:
    """Generates tweet text while ensuring it actually engages with the tweet if it's a reply."""
    
    allow_long_tweet = random.randint(1, 4) == 3  # Every 3rd or 4th tweet can be longer

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    if is_reply:
        # Ensure the tweet starts with @username if replying
        mention = f"@{username} " if username else ""
        prompt = (
            f"Reply to the following tweet in an engaging, slightly controversial way:\n"
            f"Original Tweet: {context}\n"
        )

        # Include additional context if available
        if tweet_context:
            prompt += f"Context: {tweet_context}\n"

        prompt += (
            "Your reply should:\n"
            "- Directly engage with the tweet (do NOT respond generically).\n"
            "- Be witty, insightful, or funny, depending on the tweet.\n"
            "- Be concise, keep it under 280 characters, except for every 3rd or 4th post which can be up to 500.\n"
            "- Wrap ONLY the final reply text between {{TWEET_START}} and {{TWEET_END}}.\n"
            "- Do NOT include any chain-of-thought explanation."
        )
    else:
        prompt = (
            f"Write an engaging tweet about the following topic:\n"
            f"Topic: {context}\n"
        )

        if tweet_context:
            prompt += f"Context: {tweet_context}\n"

        prompt += (
            "Your tweet should:\n"
            "- Be witty, insightful, or funny, depending on the topic.\n"
            "- Be concise, keep it under 280 characters, except for every 3rd or 4th post which can be up to 500.\n"
            "- Wrap ONLY the final tweet text between {{TWEET_START}} and {{TWEET_END}}.\n"
            "- Do NOT include any chain-of-thought explanation."
        )

    payload = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    session = requests_retry_session()
    try:
        response = session.post(url, json=payload, headers=headers, timeout=timeout, verify=True)
        response.raise_for_status()
        raw_tweet = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        extracted_tweet = extract_tweet(raw_tweet)

        # Emergency truncation (only if tweet is too long)
        if len(extracted_tweet) > 500:
            logging.warning(f"⚠️ Tweet too long ({len(extracted_tweet)} chars). Truncating...")
            extracted_tweet = extracted_tweet[:500].rstrip()

        # Ensure that replies start with @username
        if is_reply and username:
            extracted_tweet = f"@{username} {extracted_tweet}"

        return extracted_tweet

    except requests.exceptions.RequestException as e:
        logging.error(f"TogetherAI request error: {e}")
        return ""
