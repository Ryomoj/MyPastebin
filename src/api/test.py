import hashlib

sha256_hash = hashlib.new("sha256")

idd = "2"
sha256_hash.update(idd.encode())

sha256_hex = sha256_hash.hexdigest()

print(sha256_hex)