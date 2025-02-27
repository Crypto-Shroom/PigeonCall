import tweepy
import random
import os
from openai import OpenAI

# Twitter API credentials (for posting only)
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Grok API client
grok_client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# High-engagement handles
high_engagement_handles = ["VitalikButerin", "elonmusk", "brian_armstrong"]

def fetch_latest_tweet_via_grok():
    """Fetch a real, fresh tweet using Grok API."""
    handle = random.choice(high_engagement_handles)
    prompt = f"Get me the latest tweet from @{handle} posted today, February 27, 2025, with its text and real tweet ID."
    response = grok_client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    tweet_data = response.choices[0].message.content.strip()
    try:
        # Assuming Grok returns something like "Text: [tweet] | ID: [id]"
        tweet_text, tweet_id = tweet_data.split(" | ID: ")
        tweet_text = tweet_text.replace("Text: ", "")
        return {"text": tweet_text, "id": tweet_id}
    except ValueError:
        print("Error parsing tweet data. Falling back to simulation.")
        return None

def generate_reply_via_grok(tweet_text):
    """Generate a reply (max 400 chars) using Grok API."""
    prompt = f"""
    Yo, I’m @cryptoshroomog—a DeFi newbie and PhD student vibing with decentralization. Reply to this tweet: '{tweet_text}'. 
    - Toss in shroom metaphors and crypto slang like ‘degens’ or ‘HODL’.
    - Hit ‘em with a witty, brainy question about freedom or power.
    - Keep it chill, nerdy, and human—no robot vibes.
    - Max 400 chars, make folks wanna yap back.
    """
    response = grok_client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    reply = response.choices[0].message.content.strip()
    if len(reply) > 400:
        reply = reply[:397] + "..."
    return reply

def generate_essay_via_grok():
    """Generate an essay (max 4000 chars) using Grok API."""
    topics = ["DeFi ethics", "AI in crypto", "Decentralization’s societal impact"]
    topic = random.choice(topics)
    prompt = f"""
    Hey, I’m @cryptoshroomog—a crypto geek and PhD student. Write an essay on {topic}:
    - Kick off with a shroomy metaphor—like mycelium spreading.
    - Dig into what it means for society, with a playful, nerdy spin.
    - Sprinkle in slang like ‘apes’ or ‘moon’.
    - Wrap it with a big question to get folks talking.
    - Max 4000 chars, keep it real and chatty.
    """
    response = grok_client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    essay = response.choices[0].message.content.strip()
    if len(essay) > 4000:
        essay = essay[:3997] + "..."
    return essay

def main():
    """80% reply, 20% essay, using Twitter API only for posting."""
    if random.random() < 0.2:  # 20% essay
        essay = generate_essay_via_grok()
        api.update_status(status=essay)
        print("Posted essay:", essay[:100] + "..." if len(essay) > 100 else essay)
    else:  # 80% reply
        tweet = fetch_latest_tweet_via_grok()
        if tweet:
            reply = generate_reply_via_grok(tweet["text"])
            api.update_status(status=reply, in_reply_to_status_id=tweet["id"])
            print(f"Replied to tweet ID {tweet['id']}:", reply)
        else:
            print("Couldn’t fetch a tweet—something’s off with Grok’s response.")

if __name__ == "__main__":
    main()
