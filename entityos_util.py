import hashlib

def hash(data):
    hashedData = hashlib.md5(data.encode()).hexdigest()
    return hashedData


