import tkinter as tk
from gui.login_register import SecureChatApp  


if __name__ == "__main__":
    root = tk.Tk()  # This will Initialize the Tkinter root window
    app = SecureChatApp(root)  # and this will create an instance of the SecureChatApp
    root.mainloop()  # and at last it will start the Tkinter event loop
