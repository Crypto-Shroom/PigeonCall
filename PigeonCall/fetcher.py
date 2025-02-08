from bs4 import BeautifulSoup
import requests
import logging
import random
import urllib.parse

# ✅ Restored full list of valid Nitter instances
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.nl",
    "https://nitter.lucabased.xyz",
    "https://nitter.privacydev.net"
]

def fetch_nitter_results(topic: str):
    """Fetch tweets from Nitter based on a topic and extract tweet ID, text & username."""

    if not topic or topic.strip() == "":
        logging.error("❌ No topic provided for Nitter search.")
        return None, None, None

    search_query = urllib.parse.quote(topic)

    for instance in NITTER_INSTANCES:
        search_url = f"{instance}/search?f=tweets&q={search_query}"
        logging.info(f"🔍 Searching Nitter: {search_url}")

        # ✅ Restored User-Agent randomization to prevent blocking
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            response = requests.get(search_url, headers=headers, timeout=20)
            response.raise_for_status()

            if not response.text.strip():
                logging.error(f"❌ {instance} returned an empty response.")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            tweet_divs = soup.find_all("div", class_="timeline-item")

            if not tweet_divs:
                logging.warning(f"⚠️ No tweets found for topic: {topic}")
                continue

            # ✅ Select a random tweet from the latest 4 tweets
            tweet_candidates = tweet_divs[:4] if len(tweet_divs) >= 4 else tweet_divs
            selected_tweet = random.choice(tweet_candidates)

            # ✅ Extract tweet text
            tweet_text_element = selected_tweet.find("div", class_="tweet-content")
            tweet_text = tweet_text_element.get_text(strip=True) if tweet_text_element else None

            # ✅ Extract tweet ID from <a class="tweet-link" href="/username/status/1234567890#m">
            tweet_link_element = selected_tweet.find("a", class_="tweet-link")
            tweet_id = tweet_link_element['href'].split('/')[-1].split('#')[0] if tweet_link_element else None

            # ✅ Extract username
            username_element = selected_tweet.find("a", class_="username")
            username = username_element.text.strip() if username_element else None

            if tweet_text and tweet_id and username:
                logging.info(f"✅ Selected Tweet: {tweet_text} (ID: {tweet_id}, Username: {username})")
                return tweet_text, tweet_id, username

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Error fetching from {instance}: {e}")

    logging.error("❌ No tweets found across all Nitter instances.")
    return None, None, None
