import os
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

BLOCK_SIZE = 16  # AES block size in bytes

# Padding function
def pad_message(message: str) -> bytes:
    padder = padding.PKCS7(128).padder()
    return padder.update(message.encode()) + padder.finalize()

# AES ECB Encryption
def encrypt_ecb(plaintext: str, key: bytes) -> bytes:
    padded = pad_message(plaintext)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update(padded) + cipher.encryptor().finalize()

# AES CBC Encryption
def encrypt_cbc(plaintext: str, key: bytes, iv: bytes) -> bytes:
    padded = pad_message(plaintext)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    return cipher.encryptor().update(padded) + cipher.encryptor().finalize()

# Frequency Analysis (Byte Level)
def byte_frequency(ciphertext: bytes):
    return Counter(ciphertext)

# Frequency Analysis (Block Level)
def block_frequency(ciphertext: bytes):
    blocks = [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    return Counter(blocks)

# Plot Frequency Comparison
def plot_frequencies(freq_ecb, freq_cbc, title, xlabel):
    # Unified keys (all unique bytes/blocks from both ECB & CBC)
    all_keys = sorted(set(freq_ecb.keys()).union(freq_cbc.keys()))

    # Get frequencies or 0 if not present
    ecb_y = [freq_ecb.get(k, 0) for k in all_keys]
    cbc_y = [freq_cbc.get(k, 0) for k in all_keys]

    # Create labels (truncate blocks for readability)
    x_labels = [str(k) if isinstance(k, int) else k.hex()[:4] + '...' for k in all_keys]

    plt.figure(figsize=(12, 6))
    plt.bar(x_labels, ecb_y, alpha=0.6, label='ECB', color='red')
    plt.bar(x_labels, cbc_y, alpha=0.6, label='CBC', color='blue', bottom=ecb_y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


# Export frequency data to CSV
def export_to_csv(freq, filename: str):
    df = pd.DataFrame(freq.items(), columns=["Byte_or_Block", "Frequency"])
    df["Byte_or_Block"] = df["Byte_or_Block"].apply(lambda x: x.hex() if isinstance(x, bytes) else x)
    df.to_csv(filename, index=False)
    print(f"Exported frequency data to {filename}")

# --- Main Entry ---
if __name__ == "__main__":
    message = "THIS IS A REPEATED TEST MESSAGE. " * 20
    key = os.urandom(16)
    iv = os.urandom(16)

    # Encrypt using ECB and CBC
    ciphertext_ecb = encrypt_ecb(message, key)
    ciphertext_cbc = encrypt_cbc(message, key, iv)

    # Byte-level analysis
    freq_byte_ecb = byte_frequency(ciphertext_ecb)
    freq_byte_cbc = byte_frequency(ciphertext_cbc)
    plot_frequencies(freq_byte_ecb, freq_byte_cbc, "Byte-Level Frequency: ECB vs CBC", "Byte (hex)")
    export_to_csv(freq_byte_ecb, "byte_freq_ecb.csv")
    export_to_csv(freq_byte_cbc, "byte_freq_cbc.csv")

    # Block-level analysis
    freq_block_ecb = block_frequency(ciphertext_ecb)
    freq_block_cbc = block_frequency(ciphertext_cbc)
    plot_frequencies(freq_block_ecb, freq_block_cbc, "Block-Level Frequency: ECB vs CBC", "Block (hex)")
    export_to_csv(freq_block_ecb, "block_freq_ecb.csv")
    export_to_csv(freq_block_cbc, "block_freq_cbc.csv")



# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# import matplotlib.pyplot as plt
# from collections import Counter
# import os

# --- AES ECB Encryption Function ---
def aes_ecb_encrypt(plaintext: str, key: bytes) -> bytes:
    # Pad plaintext to 16-byte blocks
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()

# --- Frequency Analysis Function ---
def frequency_analysis(ciphertext: bytes):
    # Count frequency of each byte
    counter = Counter(ciphertext)
    
    # Sort and print
    print("Byte Frequency in Ciphertext:")
    for byte, freq in sorted(counter.items()):
        print(f"{byte:02x}: {freq}")
    
    # Plot
    plt.bar([f"{b:02x}" for b in counter.keys()], counter.values())
    plt.title("Frequency Analysis of Ciphertext Bytes")
    plt.xlabel("Byte (Hex)")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# --- Main ---
if __name__ == "__main__":
    # Example input
    message = "THIS IS A TEST MESSAGE REPEATED. " * 10  # repeating to simulate patterns
    key = os.urandom(16)  # AES-128 key

    print("Encrypting using AES-ECB...")
    ciphertext = aes_ecb_encrypt(message, key)
    print("Ciphertext length:", len(ciphertext))

    frequency_analysis(ciphertext)
