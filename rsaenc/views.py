import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_message(public_key, message):
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode('utf-8'))
    # Encode the encrypted message in Base64
    return base64.b64encode(encrypted_message).decode('utf-8')

def decrypt_message(private_key, encrypted_message_base64):
    private_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key)
    # Decode the Base64 encrypted message back to bytes
    encrypted_message = base64.b64decode(encrypted_message_base64)
    decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message

if __name__ == "__main__":
    private_key, public_key = generate_keys()

    message = "This is a secret message"
    encrypted_message_base64 = encrypt_message(public_key, message)
    print(f"Encrypted (Base64): {encrypted_message_base64}")

    decrypted_message = decrypt_message(private_key, encrypted_message_base64)
    print(f"Decrypted: {decrypted_message}")
