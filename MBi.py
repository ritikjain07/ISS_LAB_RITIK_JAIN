import random
import time

# Naive primality check
def is_prime_naive(n):
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Miller-Rabin test
def is_prime_mr(n, k=5):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Test a large number
n = 999331

start_naive = time.time()
result_naive = is_prime_naive(n)
end_naive = time.time()

start_mr = time.time()
result_mr = is_prime_mr(n, 5)
end_mr = time.time()

print(f"[Naive] {n} is", "prime" if result_naive else "composite", f"Time: {end_naive - start_naive:.6f}s")
print(f"[Miller-Rabin] {n} is", "probably prime" if result_mr else "composite", f"Time: {end_mr - start_mr:.6f}s")


def visualize_decomposition(n):
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    print(f"{n - 1} = {d} * 2^{r}")

# Example
visualize_decomposition(999331)



from math import gcd

def generate_large_prime(bits=16):
    while True:
        num = random.getrandbits(bits)
        if is_prime_mr(num):
            return num

def generate_rsa_keys(bits=16):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while q == p:
        q = generate_large_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)

    # Compute d
    d = pow(e, -1, phi)

    return (e, n), (d, n), (p, q)

public_key, private_key, (p, q) = generate_rsa_keys()
print("Generated RSA Keys")
print("Public Key (e, n):", public_key)
print("Private Key (d, n):", private_key)
print("Primes p, q:", p, q)
