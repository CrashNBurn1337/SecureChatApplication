import socket
import threading
import json
from encryption.encryption import encrypt_message, decrypt_message
from database.sqldatabase import DatabaseManager


class Client:
    def __init__(self, username, host="localhost", port=8765):
        self.username = username
        self.host = host
        self.port = port
        self.client_socket = None
        self.stop_event = threading.Event()
        self.messages = []

        # Fetch private key from database
        self.private_key = DatabaseManager().get_private_key(username)

    def get_recipient_public_key(self, recipient):
        """Fetch the recipient's public key."""
        return DatabaseManager().get_public_key(recipient)

    def start(self):
        """Start the client and connect to the server."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.client_socket.send(self.username.encode('utf-8'))
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
            print(f"{self.username} connected to the server.")
        except Exception as e:
            print(f"Error starting client: {e}")

    def listen_for_messages(self):
        """Listen for incoming messages."""
        while not self.stop_event.is_set():
            try:
                message = self.client_socket.recv(4096).decode('utf-8')
                if message:
                    print(f"Message received: {message}")
                    self.messages.append(message)
            except Exception as e:
                print(f"Error listening for messages: {e}")
                break

    def send_message(self, recipient, message):
        """Encrypt and send a message to the server."""
        try:
            recipient_public_key = self.get_recipient_public_key(recipient)
            encrypted_message = encrypt_message(recipient_public_key.encode(), message)
            encrypted_message_hex = encrypted_message.hex()

            data = json.dumps({
                "type": "send_message",
                "from": self.username,
                "to": recipient,
                "message": encrypted_message_hex
            })
            self.client_socket.send(data.encode('utf-8'))
            print(f"Encrypted message sent to {recipient}.")
        except Exception as e:
            print(f"Error sending encrypted message: {e}")

    def receive_messages(self):
        """Listen for incoming encrypted messages and decrypt them."""
        while not self.stop_event.is_set():
            try:
                message = self.client_socket.recv(4096).decode('utf-8')
                if message:
                    parsed_message = json.loads(message)
                    if "from" in parsed_message and "message" in parsed_message:
                        decrypted_message = decrypt_message(
                            self.private_key.encode(),
                            bytes.fromhex(parsed_message["message"])
                        )
                        self.messages.append(f"{parsed_message['from']}: {decrypted_message}")
                        print(f"Decrypted message from {parsed_message['from']}: {decrypted_message}")
            except Exception as e:
                print(f"Error receiving or decrypting message: {e}")
                break

    def stop(self):
        """Stop the client."""
        self.stop_event.set()
        if self.client_socket:
            try:
                self.client_socket.close()
                print("Client connection closed.")
            except Exception as e:
                print(f"Error closing client socket: {e}")
