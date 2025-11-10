
# 💰 Economy Manager v1

A simple and interactive **economy management system** designed for Discord bots.  
It provides tools for managing user balances, transactions, and interactive setup.

---

## 🚀 Features

- 🪙 Manage user balances (add, remove, set)
- 💬 Fully interactive setup process
- 🗃️ SQLite-link database (lightweight and portable)
- 🔒 Secure structure for easy integration with Discord bots
- 🔧 Easy installation and configuration

---

## 🧰 Installation

Run this one-line install command:

```bash
git clone https://github.com/dronzer-tb/economy-manager-v1.git && cd economy-manager-v1 && pip3 install -r requirements.txt -q && chmod +x setup-interactive.sh && ./setup-interactive.sh
````

This will:

1. Clone the repository
2. Navigate into the project directory
3. Install all dependencies
4. Launch the **interactive setup** wizard

---

## ⚙️ Manual Setup (Optional)

If you prefer to install manually, follow these steps:

```bash
# Clone the repository
git clone https://github.com/dronzer-tb/economy-manager-v1.git
cd economy-manager-v1

# Install dependencies
pip3 install -r requirements.txt

# Run interactive setup
./setup-interactive.sh
```

---

## 🧩 Directory Structure

```
economy-manager-v1/
├── bot/
│   ├── cogs/
│   │   ├── economy.py
│   │   └── __init__.py
│   ├── database/
│   │   ├── db_manager.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── config.py
│   │   └── logger.py
│   └── main.py
├── requirements.txt
├── setup-interactive.sh
├── README.md
├── LICENSE
└── VERSION
```

---

## 🧠 Interactive Setup

When you run `./setup-interactive.sh`, the setup wizard will guide you through:

* Database configuration
* Default currency setup
* Admin and bot credentials
* Optional advanced settings

All settings are saved automatically and loaded when the bot starts.

---

## 🪄 Usage

Once installed and configured, you can run the bot:

```bash
python3 bot/main.py
```

This will start your economy manager and initialize the connected database.

---

## 📦 Requirements

* Python 3.8 or later
* `pip` package manager
* Internet connection for dependency installation

---

## 🧾 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for more information.

---

## 🧑‍💻 Author

**Developed by [Dronzer](https://github.com/dronzer-tb)**
Part of the **Dronzer Studios** ecosystem.

---

## ⭐ Contributing

Contributions are welcome!
Feel free to open issues, submit pull requests, or suggest new features.

---

## 💬 Support

For bugs, feature requests, or setup help —
open an issue on the [GitHub Issues page](https://github.com/dronzer-tb/economy-manager-v1/issues).

---

**Made with ❤️ by Dronzer Studios**



