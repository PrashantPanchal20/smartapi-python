import tkinter as tk
from tkinter import ttk, messagebox

def save_credentials(username, password):
    with open("GUI\credentials.txt", "w") as file:
        file.write(f"{username},{password}")

def load_credentials():
    try:
        with open("GUI\credentials.txt", "r") as file:
            content = file.read()
            print(content)
            if content:
                return tuple(content.split(','))
    except FileNotFoundError:
        print("error")
    return None

def login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    saved_credentials = load_credentials()
    # print(saved_credentials)

    if saved_credentials and entered_username == saved_credentials[0] and entered_password == saved_credentials[1]:
        messagebox.showinfo("Login Successful", "Welcome back!")
        root.withdraw()  # Hide the login window
        # Open main application window or perform other actions
        # For simplicity, let's just reopen the login window after logout
        login_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def logout():
    root.deiconify()  # Show the login window again

def login_page():
    global username_entry, password_entry

    root.deiconify()  # Show the login window

    login_frame = ttk.Frame(root, padding=20)
    login_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

    ttk.Label(login_frame, text="Login", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
    username_entry = ttk.Entry(login_frame, font=("Helvetica", 12))
    username_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

    ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
    password_entry = ttk.Entry(login_frame, show="*", font=("Helvetica", 12))
    password_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

    login_button = ttk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=10)

    logout_button = ttk.Button(login_frame, text="Logout", command=logout)
    logout_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Load saved credentials if available
    saved_credentials = load_credentials()
    if saved_credentials:
        username_entry.insert(0, saved_credentials[0])
        password_entry.insert(0, saved_credentials[1])

    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("400x300")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", root.destroy)  # Handle window close event

    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#050505")
    style.configure("TButton", background="#4caf50", foreground="white")

    login_page()
