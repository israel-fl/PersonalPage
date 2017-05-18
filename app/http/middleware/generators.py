import os, binascii

# Generate random token
def generate_hash():
    return binascii.b2a_hex(os.urandom(15))
