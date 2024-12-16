# Secure Chat Application

<img src="asset/globe.gif" alt="Globe Animation" width="400" height="300">

A Python-based secure and anonymous peer-to-peer (P2P) chat application with encrypted messaging, designed to provide privacy-focused communication. The application supports local and cross-network communication, leveraging encryption and user authentication.

---

## Features

- **End-to-End Encryption**: All messages are encrypted to ensure secure communication.
- **User Authentication**: Registration and login functionality with encrypted local storage for user credentials.
- **Peer-to-Peer Communication**: Direct communication without reliance on centralized servers.
- **Cross-Network Functionality**: Supports communication across different networks (e.g., from one country to another).
- **Local Data Storage**: Only usernames and encrypted credentials are stored locally.
- **Dark-Themed GUI**: A modern GUI with a cybersecurity theme for ease of use.
- **Modular Design**: Components for login, registration, and chat functionality are well-structured and modular.

---

## Requirements

- Python 3.8 or higher
- Required libraries (install via `pip install -r requirements.txt`):
  - `tkinter`
  - `cryptography`
  - `websockets`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CrashNBurn1337/SecureChatApplication.git
   cd SecureChatApplication
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## Usage

1. **Registration**: Create a new account by providing a username and password. Credentials are securely stored using encryption.
2. **Login**: Log in to the application to access the chat interface.
3. **Connect to a Peer**: Enter the peer's IP address and User ID to establish a connection.
4. **Chat Securely**: Exchange encrypted messages in real-time. Messages are displayed in a chat interface, formatted with sent and received messages aligned left and right, respectively.
5. **Logout**: Safely exit the application using the logout button.

---

## Architecture

The application follows a structured development approach:

1. **Encryption**: Ensures data security during transmission and storage.
2. **WebSocket Communication**: Provides real-time, low-latency messaging between peers.
3. **Tkinter GUI**: A user-friendly graphical interface with a dark theme.
4. **Local Storage**: Stores encrypted credentials in a local database.

---

## Screenshots

### Login Screen
<img src="asset/login_registration.png" alt="Login Screen" width="400" height="300">


### Chat Interface
<img src="asset/chat_interface.png" alt="Chat Interface" width="400" height="300">
---

## Development Roadmap

- **Completed:**
  - Local network chat functionality
  - Encryption and authentication
  - GUI design and implementation

- **Planned Features:**
  - Integration with Tor network for enhanced anonymity
  - Advanced message delivery confirmation

---

## Contribution

Contributions are welcome! Feel free to submit issues, fork the repository, and create pull requests.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add YourFeature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Cryptography Module**: For providing robust encryption algorithms.
- **WebSocket Library**: For enabling real-time messaging.
- **Tkinter**: For the GUI design framework.

---

For more information, visit the [repository](https://github.com/CrashNBurn1337/SecureChatApplication).

