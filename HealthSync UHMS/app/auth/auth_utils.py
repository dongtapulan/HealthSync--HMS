import bcrypt

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed) -> bool:
    # If stored hash is invalid or not bcrypt, return False
    try:
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except ValueError:
        # Not a valid bcrypt hash
        return False
