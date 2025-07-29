import os
from cryptography.fernet import Fernet

def generate_key():
    """Generate a random encryption key"""
    return Fernet.generate_key()

def encrypt(message, key):
    """Encrypt message with key"""
    f = Fernet(key)
    return f.encrypt(message)

def decrypt(encrypted_message, key):
    """Decrypt message with key"""
    f = Fernet(key)
    return f.decrypt(encrypted_message)
