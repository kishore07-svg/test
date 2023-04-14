import argparse
import subprocess
import telebot

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--apikey', type=str, required=True, help='Telegram bot API token')
parser.add_argument('--chat_id', type=int, required=True, help='Chat ID to send contacts to')
args = parser.parse_args()

# Initialize Telebot API
bot = telebot.TeleBot(args.apikey)

# Access contacts using Termux
contact_list = subprocess.check_output(['termux-contact-list']).decode().split('\n')
contacts = [contact.split(':')[1] for contact in contact_list if 'Name' in contact]

# Send contacts to chat id using Telebot API
if len(contacts) > 0:
    message = '\n'.join(contacts)
    bot.send_message(chat_id=args.chat_id, text=message)
else:
    bot.send_message(chat_id=args.chat_id, text='No contacts found.')
