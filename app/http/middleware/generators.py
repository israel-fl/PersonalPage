import os, binascii

# Generate random token
def generate_hash(size=15):
    return binascii.b2a_hex(os.urandom(size))
