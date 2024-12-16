from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Function to generate RSA public and private keys
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Standard public exponent research from net
        key_size=2048,  # Key size for strong security 
    )
    public_key = private_key.public_key()

    # Convert private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # No password encryption
    )
    # Convert the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_key_pem, public_key_pem

# Function to encrypt a message using the recipient's public key
def encrypt_message(public_key_pem, message):
    public_key = serialization.load_pem_public_key(public_key_pem)  # Load public key from PEM
    encrypted = public_key.encrypt(
        message.encode('utf-8'),  # Convert message to bytes
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Mask generation function
            algorithm=hashes.SHA256(),  # Hashing algorithm for encryption
            label=None,
        ),
    )
    return encrypted

# Function to decrypt a message using the recipient's private key
def decrypt_message(private_key_pem, encrypted_message):
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)  # Load private key from PEM
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Mask generation function
            algorithm=hashes.SHA256(),  # Hashing algorithm for decryption
            label=None,
        ),
    )
    return decrypted.decode('utf-8')  # Convert decrypted bytes back to string
