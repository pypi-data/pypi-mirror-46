from cryptography.fernet import Fernet
from base64 import b64encode


class TextEncryptor:
    @staticmethod
    def encrypt(token, text):
        return Fernet(b64encode((token + '0' * (32 - len(token) % 32)).encode())).encrypt(text.encode())

    @staticmethod
    def decrypt(token, ciphertext):
        return Fernet(b64encode((token + '0' * (32 - len(token) % 32)).encode())).decrypt(ciphertext).decode()
