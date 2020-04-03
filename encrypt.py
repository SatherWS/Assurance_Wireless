from passlib.hash import sha256_crypt


def get_hash(user_input):
    input_hashed = sha256_crypt.hash(user_input)
    print(f"Length of hash: {len(input_hashed)}")
    if sha256_crypt.verify(user_input, input_hashed):
        return True
    return False
