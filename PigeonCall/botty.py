import logging
from config import load_config
from api_requests import find_tweet_or_topic, together_ai_generate
from twitter_api import post_tweet
from logging_setup import log_tweet_decision

# ============================ #
# 🚀 MAIN EXECUTION            #
# ============================ #

def main():
    """Main function to run the bot."""
    logging.info("🚀 Starting Twitter bot...")

    # Load configuration
    config = load_config()
    api_key, api_key_secret = config.get("Twitter", "API_KEY"), config.get("Twitter", "API_KEY_SECRET")
    access_token, access_token_secret = config.get("Twitter", "ACCESS_TOKEN"), config.get("Twitter", "ACCESS_TOKEN_SECRET")
    grok_api_key, together_api_key = config.get("GrokAI", "API_KEY"), config.get("TogetherAI", "API_KEY")


    # Determine tweet context (reply or new post)
    context, tweet_id, username, is_reply, additional_context = find_tweet_or_topic(grok_api_key) 
    if not context:
        logging.error("❌ No context found; aborting.")
        return

    # Generate tweet based on context
    tweet_text = together_ai_generate(together_api_key, context, is_reply, additional_context)
    if not tweet_text:
        logging.error("❌ No tweet generated; aborting.")
        return

    # Log decision (for transparency and debugging)
    log_tweet_decision(context, is_reply, "TogetherAI", tweet_text, tweet_id, username)

    # Post the tweet (reply if tweet_id exists)
    success = post_tweet(api_key, api_key_secret, access_token, access_token_secret, tweet_text, tweet_id)
    if not success:
        logging.error("❌ Failed to post tweet.")

if __name__ == "__main__":
    main()
