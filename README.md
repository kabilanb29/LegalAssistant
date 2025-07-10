# 🏛️📜⚖️🎓LegalBot – Discord Legal Assistant

LegalBot is an intelligent Discord bot designed to answer legal questions clearly and simply. Built using Python and OpenRouter's AI, it provides instant support inside designated channels or via slash commands.

---

## 🚀 Features

* 🤖 Auto-answer legal queries in `#legal-queries`
* ✍️ Slash command `/ask` in `#bot-commands` or DMs
* 📄 Support for long answers (auto-split)
* 🧠 Powered by OpenRouter API (LLaMA 3 model)
* 🛡️ Role-based channel permissions

---

## 🔧 Tech Stack

* Python 3.10+
* `discord.py` + `app_commands`
* OpenRouter API (LLaMA-3-8b-instruct)
* `.env` for secure config

---

## 📁 Project Structure

```
├── legal_bot.py          # Main bot code
├── .env                  # Environment secrets (never commit)
├── requirements.txt      # Python dependencies
├── README.md             # Project overview
```

---

## 🛠️ Setup on Replit

1. **Import this repo into Replit**
2. **Add ********`.env`******** file** with:

   ```env
   DISCORD_TOKEN=your_discord_bot_token
   OPENROUTER_API_KEY=your_openrouter_key
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the bot**:

   ```bash
   python legal_bot.py
   ```

✅ The bot will go online and auto-sync slash commands.

---

## 📌 Usage Guide

* Ask questions in `#legal-queries` (no commands needed)
* Use `/ask` or `/help` in `#bot-commands` or direct message
* Example: `/ask What are the rules against cyberbullying in India?`

---

## 🛡️ Channel Setup (Optional)

| Channel        | Purpose                      | Permissions                             |
| -------------- | ---------------------------- | --------------------------------------- |
| #legal-queries | Ask legal questions          | Users can send, bot replies             |
| #bot-commands  | Use slash commands like /ask | Users: slash only, Bot: manage messages |
| #general       | General discussions          | No bot replies here                     |

---

## 📜 License

MIT License – Feel free to use, modify, and share!

---

## ❤️ Contribute

Pull requests welcome! Add features, improve answers, or help with deployment.

---

## 🤖 Maintained by

**LegalBot Team** – AI meets accessibility for legal awareness.
