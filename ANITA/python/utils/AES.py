import base64
from Crypto.Cipher import AES
from .FileUtils import load_json

sk_path = "../resources/sk.json"


def __get_secret_key():
    sk = load_json(sk_path)
    return sk["secret_key"]


def encode(plain_text):
    secret_key = __get_secret_key()

    if len(plain_text) > 32:
        while len(plain_text) % 16 != 0:
            plain_text += " "

    b_plain_text = bytes(plain_text, 'utf-8').rjust(32)
    b_secret_key = bytes(secret_key, 'utf-8').rjust(32)

    cipher = AES.new(b_secret_key, AES.MODE_ECB) # never use ECB in strong systems obviously
    encoded = base64.b64encode(cipher.encrypt(b_plain_text))

    return encoded.decode('utf-8')


def decode(encrypted_text):
    secret_key = __get_secret_key()

    b_encrypted_text = bytes(encrypted_text, 'utf-8').rjust(32)
    b_secret_key = bytes(secret_key, 'utf-8').rjust(32)

    cipher = AES.new(b_secret_key, AES.MODE_ECB) # never use ECB in strong systems obviously
    decoded = cipher.decrypt(base64.b64decode(b_encrypted_text))

    return decoded.decode('utf-8').strip()
