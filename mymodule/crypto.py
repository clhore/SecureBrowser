# encoding: utf-8
# autor: Adrian Lujan Munoz (aka clhore)

# https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python
# https://stackoverflow.com/a/44126075/7553525
# https://stackoverflow.com/questions/12524994/encrypt-and-decrypt-using-pycrypto-aes-256
# https://unipython.com/cifrado-con-hashlib-de-python/
# https://es.stackoverflow.com/questions/465249/tratamiento-de-las-contrase%C3%B1as-en-el-script

# library
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, SHA512
from Crypto import Random


class CRYPTO:
    def __init__(self):
        self.password = None
        self.password_key = b''

    def encrypt_string(self, string: bytes, password: bytes):
        """
        It returns an encrypted string which can be decrypted just by the
        password.
        """
        key = self.password_to_key(password)
        IV = self.make_initialization_vector()
        encryptor = AES.new(key, AES.MODE_CBC, IV)

        # store the IV at the beginning and encrypt
        return IV + encryptor.encrypt(self.pad_string(string))

    def decrypt_string(self, string: bytes, password: bytes):
        key = self.password_to_key(password)

        # extract the IV from the beginning
        IV = string[:AES.block_size]
        decryptor = AES.new(key, AES.MODE_CBC, IV)

        string = decryptor.decrypt(string[AES.block_size:])
        return self.unpad_string(string)

    def pad_string(self, string, chunk_size=AES.block_size):
        """
        Pad string the peculirarity that uses the first byte
        is used to store how much padding is applied
        """
        assert chunk_size <= 512, 'We are using one byte to represent padding'
        to_pad = (chunk_size - (len(string) + 1)) % chunk_size
        return bytes([to_pad]) + string + bytes([0] * to_pad)

    def unpad_string(self, string):
        to_pad = string[0]
        return string[1:-to_pad]

    def encode(self, string):
        """
        Base64 encoding schemes are commonly used when there is a need to encode
        binary data that needs be stored and transferred over media that are
        designed to deal with textual data.
        This is to ensure that the data remains intact without
        modification during transport.
        """
        return base64.b64encode(string).decode("uft-8")

    def decode(self, string):
        return base64.b64decode(string.encode("uft-8"))

    @staticmethod
    def password_to_key(password):
        """
        Use SHA-256 over our password to get a proper-sized AES key.
        This hashes our password into a 256 bit string.
        """
        return SHA256.new(data=password).digest()

    @staticmethod
    def make_initialization_vector():
        """
        An initialization vector (IV) is a fixed-size input to a cryptographic
        primitive that is typically required to be random or pseudorandom.
        Randomization is crucial for encryption schemes to achieve semantic
        security, a property whereby repeated usage of the scheme under the
        same key does not allow an attacker to infer relationships
        between segments of the encrypted message.
        """
        return Random.new().read(AES.block_size)


def write_file(content: bytes, file: str):
    try: open(file, 'wb').write(content); return True
    except: return False


def content_file(file: str):
    try: return open(file, 'rb').read()
    except: return False


def encrypt_file(files: list, string_password: str):
    CRYT = CRYPTO()
    for file in files:
        write_file(CRYT.encrypt_string(
            string=content_file(file=file),
            password=bytes(string_password, encoding='utf-8')
        ), file)


def decrypt_file(files: list, string_password: str):
    CRYT = CRYPTO()
    for file in files:
        write_file(CRYT.decrypt_string(
            string=content_file(file=file),
            password=bytes(string_password, encoding='utf-8')
        ), file)


def create_hash_master_key(password_string: str):
    password_hash = SHA512\
        .new(data=password_string.encode('utf-8')).digest()
    return base64.b64encode(password_hash).decode()