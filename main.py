import random
import argparse


def setup_arguements():
    return


def is_prime(num):
    """
    The function checks if a given number is prime or not.
    
    :param num: The input number that we want to check if it is prime or not
    :return: The function `is_prime` returns a boolean value (`True` or
    `False`) depending on whether the input `num` is a prime number or not.
    """
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


def generate_prime_number(start=1000, end=10000):
    """
    This function generates a random prime number between 1000 and 10000.
    
    :param start: The starting point of the range from which the prime
    number will be generated. The default value is 1000, defaults to 1000
    (optional)
    :param end: The upper limit of the range from which the prime number
    will be generated. In this case, the range is from 1000 to 10000,
    defaults to 10000 (optional)
    :return: The function `generate_prime_number` returns a random prime
    number between the `start` and `end` values (default values are 1000 and
    10000 respectively).
    """
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num


def gcd(a, b):
    """
    The function calculates the greatest common divisor (GCD) of two numbers
    using the Euclidean algorithm.
    
    :param a: The first integer input for which we want to find the greatest
    common divisor (GCD)
    :param b: The second parameter "b" is one of the two integers for which
    we want to find the greatest common divisor (GCD) with the other integer
    "a". The function uses the Euclidean algorithm to compute the GCD of two
    integers
    :return: the greatest common divisor (GCD) of the two input integers 'a'
    and 'b'.
    """
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    """
    The function calculates the multiplicative inverse of a number using the
    extended Euclidean algorithm.
    
    :param e: The value of the public key exponent used in RSA encryption
    :param phi: phi is the value of Euler's totient function for a given
    integer n. It represents the number of positive integers less than n
    that are coprime to n
    :return: the multiplicative inverse of e modulo phi.
    """
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi


def generate_keypair():
    """
    This function generates a public-private key pair for encryption and
    decryption using the RSA algorithm.
    :return: The function `generate_keypair()` is returning a tuple of two
    tuples. The first tuple contains the public key `(e, n)` and the second
    tuple contains the private key `(d, n)`.
    """
    p = generate_prime_number()
    q = generate_prime_number()
    n = p * q

    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    """
    The function takes a public key and plaintext as input, and returns the
    encrypted ciphertext using the RSA algorithm.
    
    :param pk: The public key used for encryption, which consists of two
    values: the encryption key (key) and the modulus (n)
    :param plaintext: The plaintext is the message that needs to be
    encrypted. It is the input to the encryption function
    :return: a list of integers representing the encrypted message. Each
    integer in the list is the result of raising the ASCII value of a
    character in the plaintext to the power of the encryption key and then
    taking the modulus of the result with the encryption modulus.
    """
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    """
    This function takes a public key and a ciphertext and returns the
    decrypted plaintext using the key.
    
    :param pk: The variable "pk" is a tuple containing two integers - the
    encryption key and the modulus
    :param ciphertext: The encrypted message that needs to be decrypted
    :return: a string that represents the decrypted message.
    """
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


def main():
    public, private = generate_keypair()
    print("Public key:", public)
    print("Private key:", private)

    message = input("Enter a message to encrypt: ")
    encrypted_msg = encrypt(public, message)
    print("Encrypted message:", ''.join(map(lambda x: str(x), encrypted_msg)))

    decrypted_msg = decrypt(private, encrypted_msg)
    print("Decrypted message:", decrypted_msg)


if __name__ == '__main__':
    main()