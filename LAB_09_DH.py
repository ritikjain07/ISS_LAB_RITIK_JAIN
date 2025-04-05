from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# --- Generate Parameters (shared between both parties) ---
def generate_dh_parameters():
    return dh.generate_parameters(generator=2, key_size=2048)

# --- Generate Private and Public Key for a Party ---
def generate_private_key(parameters):
    return parameters.generate_private_key()

# --- Derive Shared Secret ---
def derive_shared_key(private_key, peer_public_key):
    shared_key = private_key.exchange(peer_public_key)

    # Derive a key using HKDF
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'dh key exchange',
    ).derive(shared_key)

    return derived_key

# --- Example Usage ---
if __name__ == "__main__":
    # Step 1: Agree on parameters
    parameters = generate_dh_parameters()

    # Step 2: Generate private/public keys for both Alice and Bob
    alice_private_key = generate_private_key(parameters)
    bob_private_key = generate_private_key(parameters)

    alice_public_key = alice_private_key.public_key()
    bob_public_key = bob_private_key.public_key()

    # Step 3: Each party computes the shared key
    alice_shared_key = derive_shared_key(alice_private_key, bob_public_key)
    bob_shared_key = derive_shared_key(bob_private_key, alice_public_key)

    # Step 4: Verify both derived the same shared key
    print("Alice's derived key: ", alice_shared_key.hex())
    print("Bob's derived key:   ", bob_shared_key.hex())
    print("Keys match:", alice_shared_key == bob_shared_key)
