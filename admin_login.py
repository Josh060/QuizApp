import tkinter as tk
from tkinter import ttk, messagebox

class AdminLogin(tk.Toplevel):
    def __init__(self, parent, success_callback):
        super().__init__(parent)
        self.title("Admin Login")
        self.success_callback = success_callback
        self.geometry("400x300")
        self.configure(bg="#f0f2f5")
        self.resizable(False, False)
        self._create_widgets()
        self.transient(parent) 
        self.grab_set()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=20, style="Card.TFrame")
        frame.pack(expand=True)
        title_label = ttk.Label(frame, text="Admin Login", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(10, 20))
        ttk.Label(frame, text="Username:", font=("Helvetica", 12)).pack(anchor="w")
        self.username_entry = ttk.Entry(frame, font=("Helvetica", 12))
        self.username_entry.pack(fill="x", pady=5)
        ttk.Label(frame, text="Password:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(fill="x", pady=5)
        self.show_password_var = tk.BooleanVar()
        show_password_cb = ttk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, command=self._toggle_password)
        show_password_cb.pack(pady=(5, 10))
        login_button = ttk.Button(frame, text="Login", command=self._attempt_login, style="Accent.TButton")
        login_button.pack(fill="x", pady=10)

    def _toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def _attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "1234":
            messagebox.showinfo("Success", "Login Successful!")
            self.success_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials. Try again.")
