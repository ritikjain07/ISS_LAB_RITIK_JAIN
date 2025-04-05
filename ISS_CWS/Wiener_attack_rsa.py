from sympy import Integer
import math

def is_perfect_square(n):
    root = int(math.isqrt(n))
    return root * root == n

def rational_to_contfrac(x, y):
    contfrac = []
    while y:
        a = x // y
        contfrac.append(a)
        x, y = y, x - a * y
    return contfrac

def convergents_from_contfrac(frac):
    convs = []
    for i in range(len(frac)):
        num, den = 1, 0
        for j in reversed(frac[:i + 1]):
            num, den = den + j * num, num
        convs.append((num, den))
    return convs

def wiener_attack(e, n):
    contfrac = rational_to_contfrac(e, n)
    convergents = convergents_from_contfrac(contfrac)

    for k, d in convergents:
        if k == 0:
            continue
        # φ(n) = (ed - 1)/k must be an integer
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        # Solve x^2 - (n - phi + 1)x + n = 0
        s = n - phi + 1
        discrim = s * s - 4 * n
        if discrim >= 0 and is_perfect_square(discrim):
            return d  # Successfully recovered d
    return None

# --- Demo Usage ---
if __name__ == "__main__":
    # Example vulnerable keys
    e = 17993
    n = 90581
    recovered_d = wiener_attack(e, n)

    if recovered_d:
        print("Private key (d) recovered:", recovered_d)
    else:
        print("Failed to recover d. Not vulnerable to Wiener's attack.")
