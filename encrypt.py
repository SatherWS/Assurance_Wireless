from flask import flash
from passlib.hash import sha256_crypt


def get_hash(unhashed_password):
    """
    Temporarily (or permanently rendered obsolete)
    """


    print(f"\tGetting hash from plaintext: {unhashed_password}")
    password_hashed = sha256_crypt.hash(unhashed_password)
    print(f"\tPassword after hash: {password_hashed}")
    print(f"\tHash help: {dir(password_hashed)}")
    print(f"\tVerifying...")
    if sha256_crypt.verify(unhashed_password, password_hashed):
        print(f"\t\tis verified, returning hash!")
        return password_hashed
    print(f"\t\tcould not be verifying, returning None!")
    return None
