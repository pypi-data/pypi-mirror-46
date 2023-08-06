from cryptography.fernet import Fernet




def generate_key_str(encoding='utf-8'):
    '''
    Generates a Fernet key string
    '''
    return Fernet.generate_key().decode(encoding)


def encrypt_str(data, key, encoding='utf-8'):
    '''
    Encrypts the supplied string data using Fernet
    '''
    cipher = Fernet(key.encode(encoding))
    return cipher.encrypt(data.encode(encoding)).decode(encoding)


def decrypt_str(data, key, encoding='utf-8'):
    '''
    Decrypts the supplied data back to string using Fernet
    '''
    cipher = Fernet(key.encode(encoding))
    return cipher.decrypt(data.encode(encoding)).decode(encoding)
