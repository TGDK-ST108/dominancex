
#!/usr/bin/env python3
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = "QQUAp".ljust(32, 'Q').encode('utf-8')
WATCH_LOG = os.path.expanduser("~/.tgdk_clipboard/stealth_watch.log")

def decrypt_line(line):
    try:
        iv_b64, ct_b64 = line.strip().split('|')
        iv = base64.b64decode(iv_b64)
        ct = base64.b64decode(ct_b64)
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ct) + decryptor.finalize()
        return padded.rstrip(b' ').decode('utf-8')
    except Exception as e:
        return f"[ERROR] {e}"

def classify(entry):
    cmd = entry.lower()
    if "tgdk" in cmd or "steelox" in cmd or "clipboard_sentinel" in cmd:
        return "TGDK_MODULE"
    elif any(term in cmd for term in ["/apex/com.android", "/system/framework", "knoxsdk"]):
        return "ANDROID_SYSTEM"
    elif "proot" in cmd or "bash -l" in cmd or "tail -f" in cmd:
        return "OFF_VECTOR"
    else:
        return "UNKNOWN"

def main():
    if not os.path.exists(WATCH_LOG):
        print("No log file found.")
        return

    with open(WATCH_LOG, 'r') as f:
        for line in f:
            dec = decrypt_line(line)
            cat = classify(dec)
            print(f"[{cat}] {dec}")

if __name__ == "__main__":
    main()

