from decryptor.utils import Utils
from decryptor.message import Message

class KeyPair:
    def __init__(self, public_key, private_key, modulus):
        self.public_key = public_key
        self.private_key = private_key
        self.modulus = modulus
    
    @staticmethod
    def from_prime_numbers(prime_p, prime_q):
        mod = prime_p * prime_q
        phi = (prime_p - 1) * (prime_q - 1)
        public_exp = Utils.public_exponent(mod, phi)
        private_exp = Utils.private_exponent(phi, mod, public_exp)

        return KeyPair(public_exp, private_exp, mod)

    def encrypt(self, message):
        content = message.to_ascii()
        encrypted_content = [num**self.public_key%self.modulus for num in content]

        return Message(encrypted_content)
    
    def decrypt(self, message):
        content = message.content
        decrypted_message = [char**self.private_key%self.modulus for char in content]

        return Message(decrypted_message)

    @staticmethod
    def break_encipher(ciphertext, hint_word, modulus):
        prime_p, prime_q = Utils.prime_factors(modulus)
        phi = (prime_p-1)*(prime_q-1)

        public_keys = Utils.public_exponent_list(modulus, phi)

        for key in public_keys:
            pair = KeyPair(key, None, modulus)
            cipherhelp = pair.encrypt(Message(hint_word))
            cipherhelp_string = ' '.join(list(map(str, cipherhelp.content)))

            if cipherhelp_string in ''.join(ciphertext.content):
                ciphertext = Message(''.join(ciphertext.content).split(' '))
                pair.private_key = Utils.generate_private_key(pair.public_key, modulus, phi)

                ciphertext.turn_int()
                plaintext = pair.decrypt(ciphertext)
                print(plaintext)

                break

