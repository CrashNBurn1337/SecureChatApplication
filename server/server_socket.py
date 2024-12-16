import socket
import threading
import json

# This is a Dictionary to track connected clients
connected_clients = {}

def handle_client(client_socket, username):
    """Handle communication with a single client."""
    connected_clients[username] = client_socket  # this will Add the client to the connected list
    try:
        while True:
            # Receivinvg data from the client 
            data = client_socket.recv(1024).decode('utf-8')
            if not data:  # If there is no data, the client will get disconnected
                break
            request = json.loads(data)

            # Handling sending message 
            if request["type"] == "send_message":
                recipient = request["to"]
                message = request["message"]

                # Sending the message to the recipient
                if recipient in connected_clients:
                    recipient_socket = connected_clients[recipient]
                    response = json.dumps({
                        "from": username,
                        "message": message
                    })
                    recipient_socket.send(response.encode('utf-8'))
    finally:
        # Removing  the client and closing the connection which was eastablished
        connected_clients.pop(username, None)
        client_socket.close()

def start_server(host="localhost", port=8765):
    """Start the chat server to accept client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # server will allow up to 5 connections total
    print(f"Server running on {host}:{port}")

    try:
        while True:
            # Accept new client connection
            client_socket, client_address = server.accept()
            username = client_socket.recv(1024).decode('utf-8')  # Get username from client
            print(f"User {username} connected from {client_address}.")
            
            # Handle the client in a different thread
            threading.Thread(target=handle_client, args=(client_socket, username), daemon=True).start()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()  # Close the server when done
        print("Server closed.")

if __name__ == "__main__":
    start_server()
