from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

# --- Key Derivation from Password ---
def derive_key(password: str, salt: bytes, key_length=32):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# --- AES Encryption ---
def encrypt(plaintext: str, password: str):
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)
    
    # Pad plaintext
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return encoded result (salt + iv + ciphertext)
    return base64.b64encode(salt + iv + ciphertext).decode()

# --- AES Decryption ---
def decrypt(encoded_ciphertext: str, password: str):
    decoded = base64.b64decode(encoded_ciphertext.encode())
    salt = decoded[:16]
    iv = decoded[16:32]
    ciphertext = decoded[32:]
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad plaintext
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

# --- Example Usage ---
if __name__ == "__main__":
    message = "This is a secret message."
    password = "strong_password_123"

    encrypted = encrypt(message, password)
    print("Encrypted:", encrypted)

    decrypted = decrypt(encrypted, password)
    print("Decrypted:", decrypted)
