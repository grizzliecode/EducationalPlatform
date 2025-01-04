import hashlib

def hash_string(input_string: str) -> str:
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the string encoded to bytes
    sha256.update(input_string.encode('utf-8'))

    # Return the hexadecimal representation of the hash
    return sha256.hexdigest()

# Example usage:
if __name__ == "__main__":
    hashed_value = hash_string("admin")
    print(hashed_value)
