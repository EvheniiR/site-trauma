import argon2
import random, string


ph = argon2.PasswordHasher(
    time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)

# Creating hash from input user's password.
def do_password_hash(password):
    hash = ph.hash(str(password))
    return hash

# Verification user's password and password hash from database.
def password_verify(hash_from_db, user_password):
    try:
        verify_valid = ph.verify(hash_from_db, str(user_password))
        return verify_valid
    except:
        return False


# Func, that creating user's token.
def random_string(stringLength=30):
    letters = string.ascii_lowercase 
    return ''.join(random.choice(letters) for i in range(stringLength))