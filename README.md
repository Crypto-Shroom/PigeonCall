# PigeonCall - 📢 Twitter AI-Engagement Bot
PigeonCall is an AI-driven Twitter bot that engages with tweets, posts insightful content, and interacts with trending discussions in chosen topics. It leverages **GrokAI** for finding discussions and **TogetherAI** for crafting engaging, human-like tweets.

GrokAI API credits are needed, but if you are using the FREE twitter API you are limited to 500 Posts a month (and 17 a day). This means that 5$ of credits will be enough for a month minimum. 

## 🚀 Features
✅ **Smart Tweet Generation** – Creates insightful, controversial, or humorous tweets.  
✅ **Context-Aware Replies** – Replies directly to tweets with relevant engagement.  
✅ **Dynamic Post Lengths** – Most tweets stay within 280 characters, but some go up to 500.  
✅ **Rate Limit Handling** – Automatically stops posting when Twitter API limits are reached.  
✅ **Modular & Configurable** – Fully customizable with separate modules for APIs, logging, and posting.  


## 🔧 Installation

```
# 1️⃣ Clone the Repository
git clone https://github.com/YOUR_GITHUB_USERNAME/PigeonCall.git
cd PigeonCall

# 2️⃣ Set Up a Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# 3️⃣ Install Dependencies
pip install -r requirements.txt

# Make sure all the files are downloaded correctly
/twitter_bot
│── bot.py               # Main execution file
│── config.py            # Configuration management
│── api_requests.py      # Handles API calls (GrokAI, TogetherAI)
│── twitter_api.py       # Twitter posting logic
│── logging_setup.py     # Logging management
│── utils.py             # Utility functions (typos, truncation, etc.)
│── config.ini           # Configuration file 

```

## 🔑 Configuration

Create a `config.ini` file in the root directory:

```
[Twitter]
API_KEY = your_api_key
API_KEY_SECRET = your_api_key_secret
ACCESS_TOKEN = your_access_token
ACCESS_TOKEN_SECRET = your_access_token_secret

[GrokAI]
API_KEY = your_grok_api_key

[TogetherAI]
API_KEY = your_together_ai_key
```

## 📝 Usage

```
# Run the bot manually
python bot.py

# Force a reply to a specific tweet
python bot.py --reply-to [tweetID] --context [give it context about the tweet]
```

## 📅 Scheduling with Cron

To automate the bot, schedule it using `cron` (Linux/macOS) or Task Scheduler (Windows). Example cronjob to run every 6 hours:

```
crontab -e
```

Add this line:

```
0 */6 * * * /path/to/your/venv/bin/python /path/to/PigeonCall/bot.py
```

## 📜 License

This project is licensed under the **European Union Public License (EUPL 1.1)**.  
See the full license here: [EUPL 1.1](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-11).

## 🤝 Contributions

Contributions, issues, and feature requests are welcome!  
Feel free to **fork** the repository and submit a **pull request**.

## 👨‍💻 Author
Developed by @Crypto-Shroom
Follow @CryptoshroomOG on X
Feel free to open an issue or submit a PR! 🚀
Solana: 4HkCpyFLHmwNt681CV8PDHtX5rRJxzUHchaxDLpuckwe
