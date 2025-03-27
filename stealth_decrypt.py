import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = "QQUAp".ljust(32, 'Q').encode('utf-8')
LOG_PATH = "stealth_watch.txt"  # or ~/.tgdk_clipboard/stealth_watch.log

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
        return f"[Error decrypting line] {e}"

with open(LOG_PATH, 'r') as f:
    for line in f:
        print(decrypt_line(line))