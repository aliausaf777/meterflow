import secrets
import string

def generate_api_key(prefix: str = "mf") -> str:
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(40))
    return f"{prefix}_{random_part}"