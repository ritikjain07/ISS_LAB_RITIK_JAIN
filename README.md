# ISS_LAB_RITIK_JAIN

## Repository Overview
This repository contains implementations of various cryptographic algorithms and security concepts as part of the Information Systems Security Laboratory coursework.

## Lab Implementations

### Symmetric Encryption

#### Classical Ciphers
1. **LAB_01_ceaserCipherJava.java**
   - Simple substitution cipher with fixed alphabet shift
   - Java implementation

2. **LAB_02_PlayfairCipher.java**
   - 5×5 grid-based substitution cipher 
   - Uses letter pairs for encryption
   - Java implementation

3. **LAB_03_HillCipher.java**
   - Matrix-based polygraphic substitution cipher
   - Uses linear algebra for encryption
   - Java implementation

4. **LAB_04_VigenereCipher.java**
   - Polyalphabetic substitution cipher
   - Uses a keyword to determine shifts
   - Java implementation

5. **LAB_05_ColumnarTranspositionCipher.java**
   - Transposition cipher that rearranges plaintext
   - Uses columns for reorganization
   - Java implementation

6. **LAB_05_railFenceCipher.java**
   - Zigzag pattern transposition cipher
   - Java implementation

#### Modern Symmetric Algorithms
7. **LAB_06_DES.PY**
   - Data Encryption Standard implementation
   - 16-round Feistel network
   - 56-bit key (64-bit with parity)
   - Python implementation

8. **LAB_07_AES.PY**
   - Advanced Encryption Standard implementation
   - Block cipher with 128/192/256-bit keys
   - Python implementation

### Asymmetric Encryption
9. **LAB_08_RSA.py**
   - RSA cryptosystem implementation
   - Public/private key pair generation
   - Message encryption and decryption
   - Using 2048-bit keys
   - Python implementation

10. **LAB_09_DH.py**
    - Diffie-Hellman key exchange protocol
    - Secure key establishment over insecure channel
    - Python implementation

## Requirements
- Java JDK 8+ (for Java implementations)
- Python 3.x (for Python implementations)
- Required Python libraries:
  - `cryptography` (for RSA, AES implementations)
  - `random` (for various algorithms)

## Usage
Each file can be run independently to demonstrate the corresponding cryptographic algorithm.

### Java files
```bash
javac LAB_XX_Algorithm.java
java LAB_XX_Algorithm

### Python files
```bash
python LAB_XX_Algorithm.py