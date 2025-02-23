import random

# Generate a random 64-bit key
def generate_des_key():
    key = ''.join(str(random.randint(0, 1)) for _ in range(64))  # 64-bit key
    return key

# Apply Parity Drop (PC-1) to get a 56-bit key
PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9, 1,
    58, 50, 42, 34, 26, 18, 10, 2,
    59, 51, 43, 35, 27, 19, 11, 3,
    60, 52, 44, 36, 63, 55, 47, 39,
    31, 23, 15, 7, 62, 54, 46, 38,
    30, 22, 14, 6, 61, 53, 45, 37,
    29, 21, 13, 5, 28, 20, 12, 4
]

def permute_key(key, table):
    return ''.join(key[i - 1] for i in table)

# Generate and permute the key
des_key = generate_des_key()
permuted_key = permute_key(des_key, PC1_TABLE)

print(f"Original 64-bit Key: {des_key}")
print(f"Permuted 56-bit Key: {permuted_key}")




# Left Circular Shift Function
def left_circular_shift(bits, shifts):
    return bits[shifts:] + bits[:shifts]

# Apply PC-1 Table
PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9, 1,
    58, 50, 42, 34, 26, 18, 10, 2,
    59, 51, 43, 35, 27, 19, 11, 3,
    60, 52, 44, 36, 63, 55, 47, 39,
    31, 23, 15, 7, 62, 54, 46, 38,
    30, 22, 14, 6, 61, 53, 45, 37,
    29, 21, 13, 5, 28, 20, 12, 4
]

# Apply PC-2 Table (for subkey generation)
PC2_TABLE = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

def permute_key(key, table):
    return ''.join(key[i - 1] for i in table)

def generate_subkeys(key):
    # Step 1: Apply PC-1 to permute the key (56 bits)
    permuted_key = permute_key(key, PC1_TABLE)

    # Step 2: Split the permuted key into two 28-bit halves
    C = permuted_key[:28]  # Left half
    D = permuted_key[28:]  # Right half

    subkeys = []
    
    # Perform left circular shifts and apply PC-2 for each of the 16 rounds
    shifts = [1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1]  # Number of shifts per round

    for i in range(16):
        # Left shift C and D
        C = left_circular_shift(C, shifts[i])
        D = left_circular_shift(D, shifts[i])
        
        # Combine C and D
        combined_key = C + D
        
        # Apply PC-2 permutation to generate the subkey (48 bits)
        subkey = permute_key(combined_key, PC2_TABLE)
        subkeys.append(subkey)

    return subkeys

# Example of key generation and left circular shifts
des_key = '1010101110001101101010101111000010111100010111100101010111100000'  # Example 64-bit key
subkeys = generate_subkeys(des_key)

# Print the subkeys generated
for i, subkey in enumerate(subkeys, 1):
    print(f"Subkey {i}: {subkey}")





# Initial Permutation (IP) Table
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Expansion (E) Table
E_TABLE = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 10, 11, 12, 13,
    14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29,
    30, 31, 32, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10, 11, 12, 13
]

# S-boxes
S_BOXES = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Permutation P (used in the Feistel function)
P_TABLE = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]

# Final Permutation (FP) Table (inverse of IP)
FP_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27
]

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)

def feistel_function(R, subkey):
    # Step 1: Expand R from 32 bits to 48 bits using the E table
    expanded_R = permute(R, E_TABLE)
    
    # Step 2: XOR with the subkey
    xor_result = bin(int(expanded_R, 2) ^ int(subkey, 2))[2:].zfill(48)
    
    # Step 3: Split into 8 blocks of 6 bits each
    blocks = [xor_result[i:i+6] for i in range(0, 48, 6)]
    
    # Step 4: Apply S-boxes
    output = ''
    for i, block in enumerate(blocks):
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        sbox_value = S_BOXES[i][row][col]  # Using all S-boxes
        output += bin(sbox_value)[2:].zfill(4)
    
    # Step 5: Apply permutation P
    permuted_output = permute(output, P_TABLE)
    
    return permuted_output

def des_encrypt(plaintext, subkeys):
    # Step 1: Apply Initial Permutation (IP) to the plaintext
    IP_plaintext = permute(plaintext, IP_TABLE)
    
    # Step 2: Split the IP result into two halves (L0, R0)
    L, R = IP_plaintext[:32], IP_plaintext[32:]
    
    # Step 3: Perform 16 Feistel rounds
    for i in range(16):
        # Feistel function on R with the subkey
        F = feistel_function(R, subkeys[i])
        
        # XOR the result of F with L to get the new L
        new_L = bin(int(L, 2) ^ int(F, 2))[2:].zfill(32)
        
        # Swap L and R for the next round
        L, R = R, new_L
    
    # Step 4: Concatenate the final L16 and R16, apply final permutation (FP)
    final_result = L + R
    ciphertext = permute(final_result, FP_TABLE)
    
    return ciphertext

# Example usage
des_key = '1010101110001101101010101111000010111100010111100101010111100000'  # Example 64-bit key
subkeys = generate_subkeys(des_key)  # Generate subkeys


plaintext = bin(int('0123456789ABCDEF', 16))[2:].zfill(64)  
print(f"Plaintext (64 bits): {plaintext}")  

subkeys = generate_subkeys(des_key)  # Generate subkeys

ciphertext = des_encrypt(plaintext, subkeys)
print(f"Ciphertext: {ciphertext}")

