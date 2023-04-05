from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt

def generate_access_token(user_id):
    dt = datetime.now(tz=timezone.utc)
    td = timedelta(minutes=5)

    with open('jwtRS256.key') as f:
        priv_key = serialization.load_pem_private_key(
            f.read().encode("utf8"), password=None, backend=default_backend()
        )

    return jwt.encode(
        {"exp": dt + td, "user_id": str(user_id), "scope": "access"},
        priv_key,
        algorithm="RS256"
    )