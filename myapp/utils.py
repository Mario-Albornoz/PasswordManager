from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

SECRET_KEY = b'0123456789abcdef0123456789abcdef'

def encrypt_password(password):
    iv = os.urandom(16)
    cipher = Cipher(
        algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()

    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted, iv

def decrypt_password(password, iv):
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(password) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()


    return unpadded_data.decode('utf8') #decode back into readible text