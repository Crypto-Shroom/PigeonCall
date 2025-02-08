# ============================ #
# 🤖 AI API REQUESTS           #
# ============================ #

import json
import random
import requests
import logging
import sys
import time
import re
import html
import config
from utils import extract_tweet_and_id, extract_tweet
from utils import requests_retry_session
from fetcher import fetch_nitter_results

# ============================ #
# 🤖 Grok API REQUESTS         #
# ============================ #

def grok_request(grok_api_key: str, prompt: str, timeout: int = 15) -> str:
    """Calls GrokAI for finding tweets to reply to or trending topics."""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {grok_api_key}", "Content-Type": "application/json"}
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

# ============================ #
# 🔍 FIND TWEET OR TOPIC       #
# ============================ #

def find_tweet_or_topic(grok_api_key: str) -> tuple:
    """Finds a tweet to reply to or a trending topic.
    
    Returns:
        - tweet_text (str): The tweet to reply to OR the trending topic.
        - tweet_id (str | None): The ID of the tweet if it's a reply, else None.
        - username (str | None): The Twitter handle of the user if it's a reply, else None.
        - context (str | None): Additional context for the tweet, if provided by AI.
        - is_reply (bool): Whether this is a reply.
    """
    if random.random() < 0.8:  # 80% chance of finding a reply-worthy tweet
        prompt = (
            "Find a highly engaging and controversial topic in crypto, politics, or cyber topics that is currently debated."
            "Prioritize topics that have strong opposing opinions and are widely mentioned. "
            "Provide ONLY the topic title and a short explanation of why it's trending, formatted as:\n"
            "Topic: <actual topic (max 3 words)>\n"
            "Context: <why it's trending>\n"
            "Do NOT generate a fake tweet or add opinions."
        )
        trending_topic = grok_request(grok_api_key, prompt)

        if not trending_topic:
            logging.error("❌ GrokAI failed to find a topic.")
            return None, None, None, None, False

        logging.info(f"🔍 Found trending topic: {trending_topic}")

        # ✅ Extract clean topic title
        logging.info("🔍 Extracting topic...")
        lines = trending_topic.split("\n")
        clean_topic = lines[0].replace("Topic:", "").strip()

        logging.info(f"🔍 Cleaned trending topic for Nitter: {clean_topic}")

        # ✅ Search for relevant tweets on Nitter
        logging.info("🔍 Attempting to search Nitter for relevant tweets...")
        tweet_text, tweet_id, username = fetch_nitter_results(clean_topic)
        if tweet_text and tweet_id and username:
            logging.info(f"✅ Using Nitter tweet: {tweet_text} is_reply={bool(tweet_id)}  (Tweet ID: {tweet_id}, Username: {username})")
            return tweet_text, tweet_id, username, trending_topic, True  # Reply case

        # ✅ Fallback: Post about the topic directly
        logging.warning("⚠️ Nitter search failed, falling back to original topic.")
        return trending_topic, None, None, trending_topic, False

    # 🌍 If no reply-worthy tweets, generate an **original** tweet
    prompt = "Find a trending topic in crypto, leftist politics, or cyber topics and explain why it's trending. Also write a short example tweet"
    topic_response = grok_request(grok_api_key, prompt)
    
    # ✅ Extract **topic and context** for TogetherAI
    topic_parts = topic_response.split("\n", 1)
    topic_text = topic_parts[0].strip()
    context = topic_parts[1].strip() if len(topic_parts) > 1 else None

    return topic_text, None, None, context, False  # New topic case


# ============================ #
# ✨ AI Tweet Generation       #
# ============================ #


def together_ai_generate(together_api_key: str, context: str, is_reply: bool, tweet_context: str, username: str = None, timeout: int = 15) -> str:
    """Generates tweet text while ensuring it actually engages with the tweet if it's a reply."""
    
    allow_long_tweet = random.randint(1, 4) == 3  # Every 3rd or 4th tweet can be longer
    tweet_length = 500 if allow_long_tweet else 280

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {together_api_key}", "Content-Type": "application/json"}

    context = re.sub(r'[^\x00-\x7F]+', ' ', context)

    if is_reply:
        if not username:
            logging.error("❌ Missing username for reply. Aborting tweet generation.")
        else:
            if username.startswith("@"):
                username = username[1:]  # Remove leading '@' if present
            logging.info(f"✅ TogetherAIAPIRequestsUsing username: @{username}")

        context = html.unescape(context)  # Convert entities like `it&#39;s` back to `it’s`
        context = context.replace("'", "’")  # Ensure apostrophes are correctly formatted

        prompt = (
            f"Reply to the following tweet in an engaging, slightly controversial way:\n"
            f"Original Tweet: {context}\n\n"
            )

        if tweet_context and isinstance(tweet_context, str):  # Only add context if it's meaningful
            prompt += f"Context: {tweet_context}\n\n"

        prompt += (
            "Your reply should simply provide the final tweet text, formatted exactly as follows:\n"
            "- Reply as if you are posting directly to Twitter.\n" 
            "- Do NOT include any analysis, reasoning, or self-reflection.\n"
            "- Directly engage with the tweet (do NOT respond generically).\n"
            "- Be witty, insightful, or funny, depending on the tweet.\n"
            f"- Keep it under {tweet_length} characters.\n"
            "- Your response MUST follow this exact format:\n\n"
            "{{TWEET_START}} Your generated tweet here {{TWEET_END}}\n\n"
            "- Do NOT include anything outside of `{{TWEET_START}}` and `{{TWEET_END}}`.\n"
            "- If you do not follow this format, your response will be ignored."
            "Only respond with the tweet inside the format below. "
            "DO NOT explain, analyze, or add anything outside of the tweet text.\n\n"
            "{{TWEET_START}} Your generated tweet here {{TWEET_END}}"
            "Before responding, analyze the tweet and form the best possible reply in your head."
            "Then, output ONLY the tweet inside the format below."
            "DO NOT include any thoughts, reasoning, or setup. ONLY output the tweet text."
            "Strictly follow this format:"
            "{{TWEET_START}} Your generated tweet here {{TWEET_END}}"
        )

    else:
        prompt = (
            f"Write an engaging tweet about the following topic:\n"
            f"Topic: {context}\n\n"
            "Your tweet should:\n"
            "- Be witty, insightful, or funny.\n"
            f"- Keep it under {tweet_length} characters.\n"
             "- Your response MUST follow this exact format:\n\n"
            "{{TWEET_START}} Your generated tweet here {{TWEET_END}}\n\n"
            "- Do NOT include anything outside of `{{TWEET_START}}` and `{{TWEET_END}}`.\n"
            "- If you do not follow this format, your response will be ignored."
        )
    if not context or context.strip() == "":
        logging.critical("🚨 Empty context detected! Exiting to prevent API waste.")
        exit(1)

    payload = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1224,
        'stream': False,
    }

    session = requests_retry_session()
    try:
        logging.info(f"🔍 TogetherAI Request Payload:\n{json.dumps(payload, indent=2)}")
        response = session.post(url, json=payload, headers=headers, timeout=timeout, verify=True)
        response.raise_for_status()
        raw_tweet = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        logging.info(f"🔍 RAW AI Response: {raw_tweet}")
        extracted_tweet = extract_tweet(raw_tweet)

        # ✅ Emergency truncation
        if len(extracted_tweet) > tweet_length:
            logging.warning(f"⚠️ Tweet too long ({len(extracted_tweet)} chars). Truncating...")
            extracted_tweet = extracted_tweet[:tweet_length].rstrip()

        return extracted_tweet

    except requests.exceptions.RequestException as e:
        logging.error(f"TogetherAI request error: {e}")
        return ""
