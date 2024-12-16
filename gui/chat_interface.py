import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import json
from encryption.encryption import encrypt_message, decrypt_message
from database.sqldatabase import DatabaseManager
import sys
import os


class ChatInterface:
    def __init__(self, root, logged_in_user, client):
        # Initialize the chat interface
        self.root = root
        self.root.title("Secure Chat")
        self.root.geometry("1000x600")
        self.root.configure(bg="#030122")

        self.logged_in_user = logged_in_user
        self.client = client
        self.contacts = []  # Stores the contact list
        self.current_contact = None  # Currently selected contact

        self.init_chat_screen()  # Setup the chat screen
        self.load_contacts()  # Load the contact list

    def init_chat_screen(self):
        """Setup the main chat interface."""
        self.clear_window()

        # Left Panel: Contacts
        self.contacts_frame = tk.Frame(self.root, width=250, bg="#030122")
        self.contacts_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            self.contacts_frame,
            text="SECCHAT",
            bg="#030122",
            fg="#00bfff",
            font=("Courier", 16, "bold")
        ).pack(pady=5)

        tk.Label(
            self.contacts_frame,
            text=f"Logged in as: {self.logged_in_user}",
            bg="#030122",
            fg="#ff0000",
            font=("Courier", 12, "italic bold")
        ).pack(pady=5)

        tk.Label(
            self.contacts_frame,
            text="Contacts",
            bg="#030122",
            fg="#00bfff",
            font=("Courier", 14, "bold")
        ).pack(pady=10)

        self.contacts_listbox = tk.Listbox(
            self.contacts_frame,
            bg="#111111",
            fg="#ffffff",
            font=("Courier", 12),
            selectbackground="#1abc9c"
        )
        self.contacts_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.contacts_listbox.bind("<<ListboxSelect>>", self.select_contact)

        # Button to refresh contacts
        refresh_button = tk.Button(
            self.contacts_frame,
            text="Refresh Contacts",
            command=self.load_contacts,
            bg="#00bfff",
            fg="#ffffff",
            font=("Courier", 12)
        )
        refresh_button.pack(fill=tk.X, padx=10, pady=5)

        # Help and Logout Buttons
        tk.Button(
            self.contacts_frame,
            text="Help",
            command=self.contact_help,
            bg="#111111",
            fg="#ffffff",
            font=("Courier", 12)
        ).pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        tk.Button(
            self.contacts_frame,
            text="Logout",
            command=self.logout,
            bg="#ff5555",
            fg="#ffffff",
            font=("Courier", 12, "bold")
        ).pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Right Panel: Chat
        self.chat_frame = tk.Frame(self.root, bg="#030122")
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.chat_label = tk.Label(
            self.chat_frame,
            text="Select a contact to start chatting",
            bg="#030122",
            fg="#00bfff",
            font=("Courier", 14)
        )
        self.chat_label.pack(pady=10)

        # Chat display area
        self.chat_display = ScrolledText(
            self.chat_frame,
            state="disabled",
            wrap=tk.WORD,
            bg="#111111",
            fg="#ffffff",
            font=("Courier", 12)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Input area for messages
        self.input_frame = tk.Frame(self.chat_frame, bg="#030122")
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.message_entry = tk.Entry(
            self.input_frame,
            font=("Courier", 12),
            bg="#111111",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            bg="#00bfff",
            fg="#ffffff",
            font=("Courier", 10, "bold"),
            width=10
        )
        send_button.pack(side=tk.RIGHT)

        # Start listening for messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def contact_help(self):
        """Show help information."""
        help_message = """
        Welcome to SECCHAT Help:
        - Select a contact to start chatting.
        - Refresh contacts to see new users.
        - Type your message and press 'Send'.
        """
        messagebox.showinfo("Help", help_message)




    def logout(self):
        """Logout and restart the application."""
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            # Stops the client and clear the current screen
            self.client.stop()
            self.clear_window()

            # Terminateing all running threads by restarting the Python process
            print("Restarting application...")
            python = sys.executable
            os.execl(python, python, *sys.argv) #This function restarts the current Python process with the same arguments (sys.argv).



    def clear_window(self):
        """Remove all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def send_message(self):
        """Send a message to the selected contact."""
        if not self.current_contact:
            messagebox.showerror("Error", "Please select a contact first!")
            return

        message = self.message_entry.get().strip()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty!")
            return

        try:
            self.client.send_message(self.current_contact, message)
            self.display_message(message, sender=self.logged_in_user)
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def receive_messages(self):
        """Receive messages from other users."""
        while True:
            if self.client.messages:
                message = self.client.messages.pop(0)
                parsed_message = json.loads(message)

                try:
                    encrypted_message = bytes.fromhex(parsed_message["message"])
                    decrypted_message = decrypt_message(
                        self.client.private_key.encode(),
                        encrypted_message
                    )
                    self.display_message(decrypted_message, sender=parsed_message["from"])
                except Exception as e:
                    print(f"Error decrypting message: {e}")
                    self.display_message("Error: Unable to decrypt message", sender=parsed_message["from"])

    def display_message(self, message, sender=None):
        """Display a message in the chat window."""
        self.chat_display.config(state="normal")
        if sender:
            self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        else:
            self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def load_contacts(self):
        """Load contacts from the database."""
        try:
            db = DatabaseManager()
            self.contacts = db.fetch_contacts(self.logged_in_user)
            self.contacts_listbox.delete(0, tk.END)
            for contact in self.contacts:
                self.contacts_listbox.insert(tk.END, contact)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {e}")

    def select_contact(self, event):
        """Select a contact from the list."""
        selection = self.contacts_listbox.curselection()
        if selection:
            self.current_contact = self.contacts_listbox.get(selection[0])
            self.chat_label.config(text=f"Chatting with {self.current_contact}")
        else:
            self.current_contact = None
            self.chat_label.config(text="Select a contact to start chatting")
