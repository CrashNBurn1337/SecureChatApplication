import unittest
from client.client import *  # Import the client implementation
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from encryption.encryption import generate_key_pair, encrypt_message, decrypt_message
import json

class TestSecureChat(unittest.TestCase):
    # Test key pair generation
    def test_generate_key_pair(self):
        # Generate private and public keys
        private_key_pem, public_key_pem = generate_key_pair()

        # Check if keys start with the correct PEM format
        self.assertTrue(private_key_pem.startswith(b"-----BEGIN PRIVATE KEY-----"))
        self.assertTrue(public_key_pem.startswith(b"-----BEGIN PUBLIC KEY-----"))

    # Test encryption and decryption
    def test_encrypt_decrypt_message(self):
        # Generate keys
        private_key_pem, public_key_pem = generate_key_pair()
        message = "Hello, Secure Chat!"

        # Encrypt and then decrypt the message
        encrypted_message = encrypt_message(public_key_pem, message)
        decrypted_message = decrypt_message(private_key_pem, encrypted_message)

        # Ensure encryption works by comparing the encrypted and original message
        self.assertNotEqual(message, encrypted_message)
        # Check if the decrypted message matches the original message
        self.assertEqual(message, decrypted_message)

    # Test sending a message
    @patch('database.sqldatabase.DatabaseManager')  # Mock the database manager
    def test_client_send_message(self, MockDatabaseManager):
        # Mock database and keys
        private_key_pem, public_key_pem = generate_key_pair()
        mock_db = MockDatabaseManager.return_value
        mock_db.get_private_key.return_value = private_key_pem.decode()
        mock_db.get_public_key.return_value = public_key_pem.decode()

        # Set up the client
        client = Client(username="Prajakta")
        client.get_recipient_public_key = MagicMock(return_value=public_key_pem.decode())
        client.client_socket = MagicMock()

        recipient = "Prajakta"
        message = "Hello, Prajakta!"

        # Call the send_message function
        client.send_message(recipient, message)

        # Check if the message was sent
        client.client_socket.send.assert_called()
        sent_data = client.client_socket.send.call_args[0][0].decode()
        sent_json = json.loads(sent_data)  # Decode the sent data

        # Validate message contents
        self.assertIn("type", sent_json)
        self.assertIn("message", sent_json)
        self.assertEqual(sent_json["to"], recipient)

    # Test receiving a message
    def test_client_receive_message(self):
        # Set up encryption keys and client
        private_key_pem, public_key_pem = generate_key_pair()
        client = Client(username="parth")
        client.private_key = private_key_pem.decode()
        encrypted_message = encrypt_message(public_key_pem, "Test Message")

        # Mock incoming data
        data = {
            "from": "parth",
            "message": encrypted_message.hex()  # Convert encrypted message to hex
        }
        client.client_socket = MagicMock()
        client.client_socket.recv = MagicMock(return_value=json.dumps(data).encode())

        # Simulate receiving messages with a patched stop_event
        with patch.object(client.stop_event, 'is_set', side_effect=[False, True]):
            client.receive_messages()

        # Check if the message was received and decrypted correctly
        self.assertTrue(len(client.messages) > 0)
        expected_message = f"{data['from']}: Test Message"
        self.assertIn(expected_message, client.messages)

# Run the tests
if __name__ == "__main__":
    unittest.main()
