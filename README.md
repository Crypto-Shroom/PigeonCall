# PigeonCall - 📢 Twitter Engagement Bot
PigeonCall is an AI-driven Twitter bot that engages with tweets, posts insightful content, and interacts with trending discussions in chosen topics. It uses GrokAI for tweet discovery, TogetherAI for responses, and includes smart rate-limit handling for seamless automation. 🚀

GrokAI API credits are needed, but if you are using the FREE twitter API you are limited to 500 Posts a month (and 17 a day). This means that 5$ of credits will be enough for a month minimum. 
Here's your README.md formatted properly for GitHub, including the EUPL 1.1 license.

md
Copy
Edit
# 🕊️ PigeonCall - AI-Powered Twitter Engagement Bot

PigeonCall is an AI-driven Twitter bot that autonomously generates tweets and replies to trending topics in **crypto, politics, and cyberculture**. It leverages **GrokAI** for finding discussions and **TogetherAI** for crafting engaging, human-like tweets.

---

## 🚀 Features

✅ **Smart Tweet Generation** – Creates insightful, controversial, or humorous tweets.  
✅ **Context-Aware Replies** – Replies directly to tweets with relevant engagement.  
✅ **Dynamic Post Lengths** – Most tweets stay within 280 characters, but some go up to 500.  
✅ **Rate Limit Handling** – Automatically stops posting when Twitter API limits are reached.  
✅ **Modular & Configurable** – Fully customizable with separate modules for APIs, logging, and posting.  

---

## 🔧 Installation

### 1️⃣ **Clone the Repository**
git clone https://github.com/YOUR_GITHUB_USERNAME/PigeonCall.git
cd PigeonCall

### 2️⃣ **Set Up a Virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

###3️⃣ ***Install Dependencies

pip install -r requirements.txt

## 🔑 Configuration
Create a config.ini file in the root directory:

[Twitter]
API_KEY = your_api_key
API_KEY_SECRET = your_api_key_secret
ACCESS_TOKEN = your_access_token
ACCESS_TOKEN_SECRET = your_access_token_secret

[GrokAI]
API_KEY = your_grok_api_key

[TogetherAI]
API_KEY = your_together_ai_key
Schedule the bot using cron (Linux/macOS) or Task Scheduler (Windows).
Example cronjob to run every 6 hours:

crontab -e
0 */6 * * * /path/to/your/venv/bin/python /path/to/PigeonCall/bot.py

## 📝 Usage
Run the bot manually:
python bot.py

## 📜 License
This project is licensed under the European Union Public License (EUPL 1.1).
See the full license here: EUPL 1.1.

## 🤝 Contributions
Contributions, issues, and feature requests are welcome!
Feel free to fork the repository and submit a pull request.

### **What's Included in This README?**
✅ **GitHub-friendly formatting**  
✅ **Installation steps with virtual environment setup**  
✅ **Cron job scheduling example**  
✅ **Usage instructions with manual execution and forced replies**  
✅ **License information (EUPL 1.1)**  
✅ **Contact & contribution guidelines**  

Let me know if you want any tweaks! 🚀
This project is European Union Public License (EUPL 1.1) Licensed 🚀

## 👨‍💻 Author
Developed by @CryptoShroom
Feel free to open an issue or submit a PR! 🚀

