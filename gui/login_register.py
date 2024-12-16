import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import hashlib
from database.sqldatabase import DatabaseManager
from encryption.encryption import generate_key_pair
from client.client import Client
from gui.chat_interface import ChatInterface
import threading
import os

class SecureChatApp: 
    def __init__(self, root):
        """Initialize the main application."""
        self.root = root
        self.root.title("Secure Chat Application")
        self.root.geometry("600x338")  # Matching the  window size with globe GIF dimensions, 
        self.root.resizable(False, False)  # Disable resizing it can be mxmized

        self.gif_path = os.path.join(os.path.dirname(__file__), "../asset/globe.gif")
        self.db_manager = DatabaseManager()  # Database manager
        self.logged_in_user = None  # it Tracks the logged-in user
        self.client = None  # Client connection instance

        self.init_login_screen()  # Start with the login screen

    def init_login_screen(self):
        """Setup the login screen."""
        self.clear_window()  # Clear any existing UI

        # Background GIF configurations size and play
        self.canvas = tk.Canvas(self.root, width=600, height=338, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.play_gif(self.gif_path)

        # Login Form configuration 
        tk.Label(self.root, text="SEC-CHAT", font=("Times New Roman", 14, "bold"), fg="#ffffff", bg="#030122").place(x=20, y=30)
        tk.Label(self.root, text="Username:", font=("Courier", 10), fg="#ffffff", bg="#030122").place(x=20, y=80)
        self.username_entry = tk.Entry(self.root, width=22, font=("Courier", 10), bg="#111111", fg="#ffffff", relief=tk.FLAT)
        self.username_entry.place(x=20, y=100)

        tk.Label(self.root, text="Password:", font=("Courier", 10), fg="#ffffff", bg="#030122").place(x=20, y=140)
        self.password_entry = tk.Entry(self.root, width=22, show="*", font=("Courier", 10), bg="#111111", fg="#ffffff", relief=tk.FLAT)
        self.password_entry.place(x=20, y=160)

        # Login and Register Buttons
        self.transparent_button(self.root, "Login", self.login, x=20, y=210)
        self.transparent_button(self.root, "Register", self.init_register_screen, x=20, y=250)

    def init_register_screen(self):
        """Setup the registration screen."""
        self.clear_window()  # Clear the UI screen

        # Background GIF
        self.canvas = tk.Canvas(self.root, width=600, height=338, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.play_gif(self.gif_path)

        # Registration Form
        tk.Label(self.root, text="Register", font=("Courier", 10), fg="#ffffff", bg="#030122").place(x=20, y=30)
        tk.Label(self.root, text="Username:", font=("Courier", 10), fg="#ffffff", bg="#030122").place(x=20, y=80)
        self.username_entry = tk.Entry(self.root, width=22, font=("Courier", 10), bg="#111111", fg="#ffffff", relief=tk.FLAT)
        self.username_entry.place(x=20, y=100)

        tk.Label(self.root, text="Password:", font=("Courier", 10), fg="#ffffff", bg="#030122").place(x=20, y=140)
        self.password_entry = tk.Entry(self.root, width=22, show="*", font=("Courier", 10), bg="#111111", fg="#ffffff", relief=tk.FLAT)
        self.password_entry.place(x=20, y=160)

        tk.Label(self.root, text="Confirm Password:", font=("Courier", 10), fg="#ffffff", bg="#030122").place(x=20, y=200)
        self.confirm_password_entry = tk.Entry(self.root, width=22, show="*", font=("Courier", 10), bg="#111111", fg="#ffffff", relief=tk.FLAT)
        self.confirm_password_entry.place(x=20, y=220)

        # Register and Back Buttons
        self.transparent_button(self.root, "Register", self.register, x=20, y=260)
        self.transparent_button(self.root, "Back to Login", self.init_login_screen, x=20, y=300)

    def login(self):
        """Handle user login."""
        username = self.username_entry.get()
        password = hashlib.sha256(self.password_entry.get().encode()).hexdigest()

        def process_login():
            if self.db_manager.authenticate_user(username, password):
                self.logged_in_user = username
                print(f"User {username} authenticated successfully.")
                self.client = Client(username)  # Initialize client
                self.client.start()
                self.clear_window()
                ChatInterface(self.root, logged_in_user=self.logged_in_user, client=self.client)
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        threading.Thread(target=process_login, daemon=True).start()

    def register(self):
        """Handle user registration."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        private_key, public_key = generate_key_pair()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if self.db_manager.register_user(username, hashed_password, public_key.decode(), private_key.decode()):
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
            self.init_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists.")

    def transparent_button(self, parent, text, command, x, y):
        """Create a button with hover effect."""
        button = tk.Label(parent, text=text, font=("Courier", 10, "bold"), fg="#ffffff", bg="#030122", cursor="hand2")
        button.place(x=x, y=y, width=150, height=20)

        def on_enter(event):
            button.config(fg="#ffffff")

        def on_leave(event):
            button.config(fg="#00bfff")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", lambda e: command())

    def play_gif(self, gif_path):
        """Play a GIF animation."""
        self.gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(Image.open(gif_path))]
        self.gif_index = 0
        self.update_gif_frame()

    def update_gif_frame(self):
        """Update the GIF animation frame."""
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.gif_frames[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.root.after(100, self.update_gif_frame)

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
