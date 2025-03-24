
import bcrypt
import random
import string


def convert_pass_to_hash(input_pass: str)  -> bytes:
    try:
        hashAndSalt = bcrypt.hashpw(input_pass.encode(), bcrypt.gensalt())
        print("successfully hashed password")
        return hashAndSalt.decode()
    except Exception as e:
        print("Hashed password failed")
        print("An error occurred:" + e)
        raise e


    
def verify_passwords(input_pass: str, hashed_pass: str) -> bool:
    valid = bcrypt.checkpw(input_pass.encode(), hashed_pass.encode())
    return valid


def generate_random_pass() -> str:
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation  # add special chars in return string

    return ''.join(random.choice(letters + digits) for i in range(random.randint(6, 10)))