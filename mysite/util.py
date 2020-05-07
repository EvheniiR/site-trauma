import argon2

def verify_password(password):
	argon2Hasher = argon2.PasswordHasher(
	    time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
	hash = argon2Hasher.hash(password)

	verifyValid = argon2Hasher.verify(hash, 'password')

	return verifyValid

print(verify_password('password'))