import logging
import tweepy
import time

# ============================
# 📲 TWITTER API INTERACTION
# ============================

def post_tweet(api_key: str, api_key_secret: str, access_token: str, access_token_secret: str, tweet_text: str, username: str = None, in_reply_to_status_id: str = None) -> bool:
    """Posts a tweet or a reply using Twitter API v2.

    Args:
        - api_key (str): Twitter API key.
        - api_key_secret (str): Twitter API key secret.
        - access_token (str): Twitter access token.
        - access_token_secret (str): Twitter access token secret.
        - tweet_text (str): The text of the tweet.
        - username (str, optional): The username of the tweet being replied to.
        - in_reply_to_status_id (str, optional): The ID of the tweet being replied to.

    Returns:
        - bool: True if tweet was successful, False otherwise.
    """
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_key_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # ✅ **Check Rate Limit Before Posting**
    if not check_rate_limit(client):
        logging.error("⏳ Skipping tweet due to rate limits.")
        return False

    try:
        # ✅ Ensure username is included in replies
        if in_reply_to_status_id and username:
            username = username.lstrip("@")  # ✅ Remove extra '@' if present
            if not tweet_text.startswith(f"@{username} "):
                tweet_text = f"@{username} {tweet_text.lstrip()}"  # ✅ Ensure proper spacing & formatting
            response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=in_reply_to_status_id)
            logging.info(f"✅ Reply posted successfully: {tweet_text} (Replying to {in_reply_to_status_id})")
        else:
            response = client.create_tweet(text=tweet_text)
            logging.info(f"✅ Tweet posted successfully: {tweet_text}")

        return True

    except tweepy.errors.TooManyRequests:
        logging.error("❌ 429 Too Many Requests: Rate limit reached.")
        logging.info("⏳ Exiting and retrying at next scheduled time.")
        exit()
        return False

    except tweepy.TweepyException as e:
        logging.error(f"❌ Error posting tweet: {e}")
        return False
    

# ============================
# 📲 TWITTER RATE LIMIT CHECK
# ============================

def check_rate_limit(client: tweepy.Client) -> bool:
    """Checks Twitter API v2 rate limits and stops execution if limits are reached."""
    try:
        # Make a test request to check rate limit headers
        response = client.get_me()

        # Verify response headers exist
        if response and hasattr(response, "headers"):
            remaining = int(response.headers.get("x-rate-limit-remaining", 1))
            reset_time = int(response.headers.get("x-rate-limit-reset", time.time()))

            logging.info(f"🛑 Twitter Rate Limit: {remaining} tweets remaining. Reset time: {reset_time}")

            # If rate limit is reached, stop execution
            if remaining <= 0:
                reset_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))
                logging.error(f"⚠️ Rate limit exceeded. Bot will stop execution. Next reset: {reset_timestamp}")
                exit(1)  # Stop the bot

            return True  # Continue execution if rate limit is not exceeded

    except tweepy.TweepyException as e:
        logging.error(f"⚠️ Could not fetch rate limits: {e}")
        return False  # Default to stopping if we can't determine rate limits

    return True  # Default to allowing the tweet if headers are missing
