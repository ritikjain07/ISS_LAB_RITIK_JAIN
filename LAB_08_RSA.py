from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

# --- Generate RSA Keys ---
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

# --- Serialize Keys to PEM Format ---
def serialize_keys(private_key, public_key):
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

# --- Encrypt Message ---
def encrypt_message(message: str, public_key):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()

# --- Decrypt Message ---
def decrypt_message(encrypted_message: str, private_key):
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message.encode()),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# --- Example Usage ---
if __name__ == "__main__":
    # Generate RSA key pair
    private_key, public_key = generate_keys()

    # Example message
    message = "This is a top-secret message."

    # Encrypt
    encrypted_msg = encrypt_message(message, public_key)
    print("Encrypted Message:\n", encrypted_msg)

    # Decrypt
    decrypted_msg = decrypt_message(encrypted_msg, private_key)
    print("Decrypted Message:\n", decrypted_msg)
