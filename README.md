<p align="center">
  <img src="image.png" alt="Mafia Bot Banner" width="100%">
</p>

<h1 align="center">🎭 Mafia Bot</h1>

<p align="center">
<b>Play. Lie. Win.</b>
</p>

<p align="center">
A modern Telegram bot that fully automates the classic <b>Mafia</b> party game in Telegram groups.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/aiogram-3.x-26A5E4?style=for-the-badge&logo=telegram&logoColor=white">
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
<img src="https://img.shields.io/github/stars/Kamron5505/Mafia-bot?style=for-the-badge">
<img src="https://img.shields.io/github/license/Kamron5505/Mafia-bot?style=for-the-badge">
</p>

---

# 📖 About

**Mafia Bot** is a fully automated Telegram bot that brings the classic Mafia game to Telegram.

The bot automatically manages every stage of the game:

- 🎮 Create game rooms
- 👥 Player management
- 🎭 Automatic role distribution
- 🌙 Night phase
- ☀️ Day phase
- 🗳️ Voting system
- 🏆 Automatic winner detection

---

# ✨ Features

| Feature | Status |
|---------|:------:|
| Create Game Rooms | ✅ |
| Join Games | ✅ |
| Automatic Role Distribution | ✅ |
| Night Phase | ✅ |
| Day Phase | ✅ |
| Voting System | ✅ |
| Win Detection | ✅ |
| Telegram Commands | ✅ |
| Docker Support | ✅ |

---

# 🚀 Quick Start

## Clone the repository

```bash
git clone https://github.com/Kamron5505/Mafia-bot.git
cd Mafia-bot
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python bot.py
```

---

# 🐳 Docker

```bash
docker compose up --build
```

or

```bash
docker-compose up --build
```

---

# ⚙️ Environment Variables

Create a `.env` file.

```env
BOT_TOKEN=YOUR_BOT_TOKEN
```

---

# 🛠 Tech Stack

- Python
- aiogram
- SQLite
- Docker
- Docker Compose

---

# 📂 Project Structure

```text
Mafia-bot/
│
├── database/
├── handlers/
├── keyboards/
├── roles/
├── utils/
├── bot.py
├── config.py
├── image.png
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 📜 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show available commands |
| `/create` | Create a game |
| `/join` | Join a game |
| `/leave` | Leave the game |

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

# ⭐ Support

If you like this project, don't forget to leave a ⭐ on GitHub!

---

<div align="center">

Made with ❤️ by **Kamron Fazilov**

</div>
