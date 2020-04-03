#!/usr/bin/env python
import hashlib


def get_cipher(user_input):
    message_hashed = hashlib.md5(user_input.encode())
    cipher = message_hashed.hexdigest()
    return cipher
