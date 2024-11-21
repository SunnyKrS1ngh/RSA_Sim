import random
import math
import multiprocessing

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def generate_prime_in_range(args):
    min_value, max_value = args
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def generate_keys_parallel(min_value=1000, max_value=50000):
    with multiprocessing.Pool(processes=2) as pool:
        p, q = pool.map(generate_prime_in_range, [(min_value, max_value)] * 2)
    
    while p == q:
        q = generate_prime_in_range((min_value, max_value))

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(3, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)

    d = mod_inverse(e, phi_n)

    return (e, n), (d, n)  # Public key, Private key

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Modular inverse does not exist!")

def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(ch), e, n) for ch in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return "".join(chr(pow(ch, d, n)) for ch in ciphertext)
