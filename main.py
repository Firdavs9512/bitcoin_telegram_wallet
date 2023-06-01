import telebot
import time
from Bitcoin import check_balance, send, user_check, transactions_list
from config import token

# Create a new Telegram bot instance
bot = telebot.TeleBot(token)

# Dictionary to store user states
user_state = {}


# Handler for the "/start" command
@bot.message_handler(commands=["start"])
def handle_start(message):
    # Send a welcome message
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    balance_button = telebot.types.KeyboardButton("Information 💎")
    send_button = telebot.types.KeyboardButton("Send 📤")
    transactions_button = telebot.types.KeyboardButton("Transactions 📑")
    markup.add(balance_button, send_button, transactions_button)
    # markup.add(send_button)
    # Create new user account
    user_check(message.from_user.id)
    bot.send_message(
        message.chat.id,
        "Welcome to Bitcoin wallet bot! How can I assist you?",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "Transactions 📑")
def handle_transactions(message):
    if user_state.get(message.chat.id) == "waiting_transactions":
        return

    # Set the user state to 'waiting_transactions'
    user_state[message.chat.id] = "waiting_transactions"

    wait_message = bot.send_message(message.chat.id, "⏱ Please wait...")
    transactions = transactions_list(message.from_user.id)

    # Delete the "Please wait!" message
    bot.delete_message(wait_message.chat.id, wait_message.message_id)

    del user_state[message.chat.id]
    # Send the balance to the user
    for t in transactions:
        bot.send_message(
            message.chat.id,
            f"Address: {t['address']} \nAmount: {t['value']} \nTransaction id: `{t['txid']}` \nConfirmation: {t['confirmations']}",
            parse_mode="Markdown",
        )


# Handler for the "Balance" button
@bot.message_handler(func=lambda message: message.text == "Information 💎")
def handle_balance(message):
    # Check if the user is already waiting for balance retrieval
    if user_state.get(message.chat.id) == "waiting_balance":
        return

    # Set the user state to 'waiting_balance'
    user_state[message.chat.id] = "waiting_balance"

    # Send a "Please wait!" message
    wait_message = bot.send_message(message.chat.id, "⏱ Please wait...")

    balance = check_balance(message.from_user.id)

    # Delete the "Please wait!" message
    bot.delete_message(wait_message.chat.id, wait_message.message_id)

    del user_state[message.chat.id]
    # Send the balance to the user
    bot.send_message(message.chat.id, balance, parse_mode="Markdown")


# Handler for the "Cancel" button
@bot.message_handler(func=lambda message: message.text == "Cancel ❌")
def handle_send(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    balance_button = telebot.types.KeyboardButton("Information 💎")
    send_button = telebot.types.KeyboardButton("Send 📤")
    transactions_button = telebot.types.KeyboardButton("Transactions 📑")
    markup.add(balance_button, send_button, transactions_button)
    # Ask the user for the address
    bot.reply_to(message, "❌ Canceled!", reply_markup=markup)


# Handler for the "Send" button
@bot.message_handler(func=lambda message: message.text == "Send 📤")
def handle_send(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    cancel_button = telebot.types.KeyboardButton("Cancel ❌")
    markup.add(cancel_button)
    # Ask the user for the address
    bot.reply_to(message, "📤 Please enter the address to send to:", reply_markup=markup)


# Handler for receiving the address
@bot.message_handler(func=lambda message: True)
def handle_address(message):
    address = message.text

    # Ask the user for the amount
    bot.reply_to(
        message,
        "💳 Please enter the amount to send:",
    )

    # Register a new handler for receiving the amount
    bot.register_next_step_handler(message, handle_amount, address)


# Handler for receiving the amount
def handle_amount(message, address):
    amount = message.text

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    balance_button = telebot.types.KeyboardButton("Information 💎")
    send_button = telebot.types.KeyboardButton("Send 📤")
    transactions_button = telebot.types.KeyboardButton("Transactions 📑")
    markup.add(balance_button, send_button, transactions_button)

    # Process the address and amount
    # Waiting for sending
    if user_state.get(message.chat.id) == "waiting_send":
        return

    # Set the user state to 'waiting_balance'
    user_state[message.chat.id] = "waiting_send"

    # Send a "Please wait!" message
    wait_message = bot.send_message(message.chat.id, "⏱ Please wait...")

    try:
        t = send(message.from_user.id, address, amount)
    except:
        t = "❌ Error for sending!"

    # Delete the "Please wait!" message
    bot.delete_message(wait_message.chat.id, wait_message.message_id)

    # Replace this with your actual send logic
    del user_state[message.chat.id]
    # Send the confirmation message to the user
    bot.send_message(message.chat.id, t, reply_markup=markup)


# Start the bot
bot.infinity_polling()
