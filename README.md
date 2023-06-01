# Telegram Bitcoin TestNet Wallet Bot

This is a Telegram bot that allows you to manage your Bitcoin wallet. The bot provides features such as checking your balance, sending Bitcoin to a specified address, and listing your transaction history.

## Prerequisites

Before running the bot, make sure you have the following:

- Python 3 installed
- `telebot` library installed (`pip install pyTelegramBotAPI`)
- `Bitcoin` module for handling Bitcoin-related operations
- `config` module with your Telegram bot token

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Firdavs9512/bitcoin_telegram_wallet.git
cd bitcoin_telegram_wallet
```

2. Install the required dependencies:

For linux install this:
```bash
sudo apt install -y postgresql postgresql-contrib mysql-server libpq-dev libmysqlclient-dev
```
Install all requiremenst
```bash
pip install -r requirements.txt
```

3. Create new file `config.py` and save this values:
```python
database = 'telegram.db'              # sqlite database url
token = 'telegram_bot_token'          # botfather bot token
network='testnet'                     # Crypto network
prefix = 'test'                    # Using prefix for save
```

## Usage

To start the bot, run the following command:

```bash
python bot.py
```

## Available Commands

The bot supports the following commands and features:

- `/start`: Initializes the bot and displays the main menu.
- **Information**: Retrieves your Bitcoin wallet balance.
- **Send**: Allows you to send Bitcoin to a specified address.
- **Transactions**: Lists your transaction history.

## Worker bot

The URL of the currently running bot: [@bitcoin_network_testnetbot](https://t.me/bitcoin_network_testnetbot)
Creator: Firdavs
