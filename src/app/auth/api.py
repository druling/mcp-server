from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.utils import base64url_encode
from fastapi import APIRouter

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.get("/.well-known/jwks.json")
def jwks():
    pub = serialization.load_pem_public_key("PUBLIC_KEY")
    numbers: rsa.RSAPublicNumbers = pub.public_numbers()

    def b64(n: int):
        return base64url_encode(
            n.to_bytes((n.bit_length() + 7) // 8, "big")
        ).decode()

    return {
        "keys": [{
            "kty": "RSA",
            "use": "sig",
            "kid": "KEY_ID",
            "alg": "ALG",
            "n": b64(numbers.n),
            "e": b64(numbers.e),
        }]
    }
