from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keys() -> tuple[str, str]:
    """
    Generates a pair of RSA keys, a public key and a private key.

    :returns: A tuple containing the private key and public key in PEM format, both as strings.
    """
    # Generate private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    # Get public key from private key
    public_key = private_key.public_key()

    # Convert private key to PEM format
    private_pem: str = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    # Convert public key to PEM format
    public_pem: str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_pem, public_pem
