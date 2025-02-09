import os
import random
import logging
import requests
import tweepy
from configparser import ConfigParser
from google.api_core import exceptions as google_api_exceptions
from google.oauth2 import service_account
import google.generativeai as genai
import time


# Logging setup (adjust as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ============================
# 🛠 CONFIGURATION MANAGEMENT
# ============================

def ensure_utf8_config(file_path: str) -> None:
    with open(file_path, 'r', encoding='ascii', errors='ignore') as f:
        content = f.read()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_config() -> ConfigParser:
    base_path = os.path.dirname(__file__)
    config_path = os.path.join(base_path, 'config.ini')
    ensure_utf8_config(config_path)

    config = ConfigParser(interpolation=None)
    config.read(config_path, encoding='utf-8')
    return config


# ============================
# 🤖 Gemini API REQUESTS
# ============================

def gemini_generate_text(config, prompt: str, model_name: str = "{model_name}", temperature: float = 0.7) -> str:
    gemini_api_key = config.get("Gemini", "API_KEY")
    genai.configure(api_key=gemini_api_key)

    try:
        model = genai.GenerativeModel(model_name)

        # Create a GenerationConfig object to set parameters:
        generation_config = genai.GenerationConfig(temperature=temperature)

        response = model.generate_content(prompt, generation_config=generation_config)

        if response.text:
            return response.text
        else:
            logging.error(f"Gemini API returned an empty response: {response}")
            return ""

    except genai.ResourceExhaustedError as e:  # Correct exception class
        logging.error(f"Gemini API rate limit reached: {e}")
        return ""
    except Exception as e:
        logging.error(f"Gemini API request error: {e}")
        return ""
    
def extract_tweet(raw_output: str) -> str:
    """
    Finds text between {{TWEET_START}} and {{TWEET_END}}.
    Falls back to returning raw_output if markers aren't found.
    """
    start_marker = "{{TWEET_START}}"
    end_marker = "{{TWEET_END}}"

    lower_output = raw_output.lower()
    start_idx = lower_output.find(start_marker.lower())
    end_idx = lower_output.find(end_marker.lower())

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return raw_output[start_idx + len(start_marker) : end_idx].strip()
    else:
        return raw_output.strip()

def generate_tweet_text(config, model_name) -> str:
    """
    Generates a casual, slightly controversial, and meaningful reply tweet about a trending crypto post.
    """
    # Dynamically determine tweet length (between 140 and 280 characters)
    tweet_length = random.randint(180, 500)  # Or adjust range as needed

  #
  # Replace the prompt according to own preferences
  #
  
    prompt = (
        "You are an advanced tweet generator AI. Your task is to produce a single, top-tier tweet crypto mushroom or politics topic that responds to a "
        "trending post in a deep and meaningful way or in a shitpost stile. Be creative, bold etc. Try out things. This tweet must:\n"
        "1) Contain ONLY one purposeful spelling mistake (for an authentic vibe), but make sure the spelling mistake is not in the hashtags.\n"
        "2) Be slightly controversial, sarcastic, or comedic. \n"
        "4) shows a deeper philosophical or political angle or be outrageous.\n"
        "5) Use at least one relevant hashtag (e.g., #crypto, #mushroom, #politics, #philosophy, etc.).\n"
        "6) Use at least one emoji.\n"
        "7) helps getting Think Kaito Yaps.\n"
        "8) Avoid typical engagement cliches.\n"
        "8) Place ONLY the final tweet text between {{TWEET_START}} and {{TWEET_END}}.\n"
        f"9) Fit within {tweet_length} characters total.\n"
        "10) Output nothing else beyond the tweet text in those markers, and do NOT include chain-of-thought or extra reasoning.\n"
    )

    # Call Gemini (or your LLM) with the prompt
    raw_response = gemini_generate_text(config, prompt, model_name=model_name)
    extracted_tweet = extract_tweet(raw_response)
    final_tweet = extracted_tweet
    
    # Enforce 280-character limit
    if len(final_tweet) > tweet_length:
        logging.warning("Generated tweet exceeds {tweet_length} characters. Truncating.")
        final_tweet = final_tweet[:tweet_length].rstrip()

    return final_tweet


def post_tweet_legacy(
    api_key: str,
    api_key_secret: str,
    access_token: str,
    access_token_secret: str,
    tweet_text: str
) -> bool:
    """
    Posts the tweet using OAuth 1.0a credentials against the Twitter API v2.
    """
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_key_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    try:
        response = client.create_tweet(text=tweet_text)
        if response and response.data and "id" in response.data:
            logging.info("Tweet posted successfully: %s", tweet_text)
            return True
        else:
            logging.error("Unexpected Twitter API response: %s", response)
            return False
    except tweepy.TweepyException as e:
        if e.response is not None and e.response.status_code == 429: # Check the status code directly
            logging.error(f"Rate limit exceeded: {e}")

            # Use the provided reset time if available
            if 'x-rate-limit-reset' in e.response.headers:  # Check for reset header
                reset_time = int(e.response.headers['x-rate-limit-reset'])
            else: # Fallback to using current time + default retry duration
                reset_time = int(time.time()) + 900 # set a default of 15 min, as 900 seconds
            sleep_duration = reset_time - int(time.time()) + 60  # Extra buffer

            logging.info(f"Sleeping for {sleep_duration} seconds...")
            time.sleep(sleep_duration)

            # Retry posting after the sleep (recursive call – be careful with this)
            return post_tweet_legacy(api_key, api_key_secret, access_token, access_token_secret, tweet_text)

        else: # Handle other Tweepy errors
            logging.error(f"Error posting tweet: {e}")
            return False
        
# ============================
# 📲 TWITTER API INTERACTION
# ============================
        
def main():
    config = load_config()

    # Twitter credentials
    api_key = config.get("Twitter", "API_KEY")
    api_key_secret = config.get("Twitter", "API_KEY_SECRET")
    access_token = config.get("Twitter", "ACCESS_TOKEN")
    access_token_secret = config.get("Twitter", "ACCESS_TOKEN_SECRET")


    gemini_model = config.get("Gemini", "MODEL")
    tweet_text = generate_tweet_text(config, gemini_model)

    if not tweet_text:
        logging.error("No tweet generated; aborting.")
        return

    success = post_tweet_legacy(api_key, api_key_secret, access_token, access_token_secret, tweet_text)
    if not success:
        logging.error("Failed to post tweet.")

if __name__ == "__main__":
    main()
