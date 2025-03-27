import psutil
import time
import os
import base64
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

WATCH_LOG = os.path.expanduser("~/.tgdk_clipboard/stealth_watch.log")
KEY = "QQUAp".ljust(32, 'Q').encode('utf-8')

# Patterns to detect
WATCH_KEYWORDS = [
    'netcat', 'ncat', 'nc', 'bash -i', 'sh -i', 'clipboard', 'copyq', 'xclip', 'parcellite',
    'reverse shell', 'socat', 'clipboard_sentinel.py', 'subprocess', 'socket'
]

def qquap_encrypt(text):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = text + ' ' * (16 - len(text) % 16)
    ct = encryptor.update(padded.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(iv).decode() + "|" + base64.b64encode(ct).decode()

def log_event(event):
    enc = qquap_encrypt(event)
    with open(WATCH_LOG, 'a') as f:
        f.write(enc + '\n')

def scan_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            full_cmd = ' '.join(proc.info['cmdline']).lower()
            if any(keyword in full_cmd for keyword in WATCH_KEYWORDS):
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_event(f"{ts} :: Suspicious Process PID {proc.pid}: {full_cmd}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    while True:
        scan_processes()
        time.sleep(8)