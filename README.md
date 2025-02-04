# PigeonCall - 📢 Twitter Engagement Bot
PigeonCall is an AI-driven Twitter bot that engages with tweets, posts insightful content, and interacts with trending discussions in chosen topics. It uses GrokAI for tweet discovery, TogetherAI for responses, and includes smart rate-limit handling for seamless automation. 🚀

GrokAI API credits are needed, but if you are using the FREE twitter API you are limited to 500 Posts a month (and 17 a day). This means that 5$ of credits will be enough for a month minimum. 

#📌 Features
✔ Engages with tweets in the crypto, political, and cybersecurity space
✔ Finds trending topics and posts tweets accordingly
✔ Ensures replies actually reply to the intended tweet & mentions the user
✔ Randomized tweet length (some posts are long-form for better engagement)
✔ Rate limit detection (stops execution if Twitter API limits are reached)
✔ Scheduled execution via cronjob

#🚀 Installation
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/twitter-engagement-bot.git
cd twitter-engagement-bot/bot_splitted
2️⃣ Create a Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
or for Windows:

bash
Copy
Edit
.venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
⚙️ Configuration
1️⃣ Set Up API Keys in config.ini
Create a config.ini file in the bot_splitted/ directory:

ini
Copy
Edit
[Twitter]
API_KEY = your_twitter_api_key
API_KEY_SECRET = your_twitter_api_secret
ACCESS_TOKEN = your_twitter_access_token
ACCESS_TOKEN_SECRET = your_twitter_access_token_secret

[GrokAI]
API_KEY = your_grok_api_key

[TogetherAI]
API_KEY = your_together_ai_key
⚠ Important: Never share this file! Add it to .gitignore before pushing to GitHub.

#🎯 Running the Bot
Run the bot manually with:

bash
Copy
Edit
python bot.py
Or to force a reply to a specific tweet:

bash
Copy
Edit
python bot.py --reply-to 1735867223591234567 --context "Bitcoin is digital gold."
📅 Scheduling with Cronjob
To automate the bot, add it to your crontab:

bash
Copy
Edit
crontab -e
Then add a job to run every 4 hours (adjust based on rate limits):

bash
Copy
Edit
0 */4 * * * /path/to/venv/bin/python /path/to/twitter-bot/bot_splitted/bot.py >> /path/to/twitter-bot/bot_splitted/logs.txt 2>&1
✅ This ensures it runs automatically and logs output.

#🛠 Troubleshooting
🔹 API Rate Limit Error (429)
✔ Bot stops execution if rate limit is hit (will restart via cronjob)

🔹 Error: Missing config.ini
✔ Ensure your API keys are properly set up in config.ini

🔹 Bot does not post replies correctly
✔ Check logs for extracted tweet ID & username

#📜 License
This project is European Union Public License (EUPL 1.1) Licensed 🚀

👨‍💻 Author
Developed by @CryptoShroom
Feel free to open an issue or submit a PR! 🚀

