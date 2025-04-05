import random

def is_prime(n, k=5):
    """ Miller-Rabin Primality Test
    n: number to test
    k: number of accuracy rounds
    """
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Write n-1 as d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Run test k times
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
            return False  # Composite

    return True  # Probably Prime

# --- Example usage ---
if __name__ == "__main__":
    test_numbers = [561, 1105, 1729, 7919, 104729, 999331]
    for num in test_numbers:
        print(f"{num} is", "probably prime" if is_prime(num) else "composite")
