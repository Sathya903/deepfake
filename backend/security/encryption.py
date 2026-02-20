from cryptography.fernet import Fernet
import os

key = os.getenv("FILE_ENCRYPTION_KEY")

if key is None:
    raise ValueError("FILE_ENCRYPTION_KEY not set in environment variables")

cipher = Fernet(key.encode())


def save_encrypted_file(file_bytes, file_path):
    encrypted_data = cipher.encrypt(file_bytes)

    with open(file_path, "wb") as f:
        f.write(encrypted_data)


def load_encrypted_file(file_path):
    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data