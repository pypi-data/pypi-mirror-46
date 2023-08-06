from math import gcd
from random import choice

class Utils:

    @staticmethod
    def prime_factors(prime_product):
        initial_value = 2
        prime_factors = []

        while initial_value ** 2 <= prime_product:
            if prime_product % initial_value:
                initial_value += 1
            else:
                prime_product //= initial_value 
                prime_factors.append(initial_value)
        if prime_product > 1:
            prime_factors.append(prime_product)

        return (prime_factors[0], prime_factors[1])

    @staticmethod
    def eucledian(num, mod):
        return gcd(num, mod)

    @staticmethod
    def is_coprime(a, b):
        return Utils.eucledian(a, b) == 1

    @staticmethod
    def public_exponent_list(mod, phi):
        return [e for e in range(2, phi) if Utils.is_coprime(e, mod) and Utils.is_coprime(e, phi)]

    @staticmethod
    def public_exponent(mod, phi):
        return choice(Utils.public_exponent_list(mod, phi))

    @staticmethod
    def private_exponent_list(phi, mod, public_exponent):
        return [d for d in range(2, mod) if (d*public_exponent-1) % phi == 0]
    
    @staticmethod
    def private_exponent(phi, mod, public_exponent):
        return choice(Utils.private_exponent_list(phi, mod, public_exponent))

    @staticmethod
    def generate_private_key(public_exponent, mod, phi):
        for private_exponent in range(2, mod):
            if not (private_exponent*public_exponent-1) % phi:
                return private_exponent