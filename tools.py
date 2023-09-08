from cryptography.fernet import Fernet
import openai

class Encryption:

    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, message):
        encMessage = self.fernet.encrypt(message.encode())
        return encMessage

    def decrypt(self, encrypted_text):
        decMessage = self.fernet.decrypt(encrypted_text).decode()
        return decMessage

"""
# Example usage:
if __name__ == "__main__":
    # Replace 'your_secret_key_here' with your actual secret key
    secret_key = b'your_secret_key_here'

    # Create an Encryption object with the secret key
    encryptor = Encryption(secret_key)

    # Encrypt a message
    message = "Hello, world!"
    encrypted_message = encryptor.encrypt(message)
    print("Encrypted string:", encrypted_message)

    # Decrypt the encrypted message
    decrypted_message = encryptor.decrypt(encrypted_message)
    print("Decrypted string:", decrypted_message)
    



"""

import openai

class Response_engine:

    def __init__(self, api_key):
        self.api_key = api_key

    def speaking_engine(self, user_input):
        openai.api_key = self.api_key

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"talk like case in interstellar {user_input}",
            max_tokens=1000,
        )
        print(response)

