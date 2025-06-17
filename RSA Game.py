import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from math import gcd

# ===== Utility Functions =====

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_e(phi_n):
    e_list = [e for e in range(3, phi_n, 2) if gcd(e, phi_n) == 1]
    return random.sample(e_list, min(5, len(e_list)))

def modinv(a, m):
    # Extended Euclidean Algorithm
    m0, x0, x1 = m, 0, 1
    if gcd(a, m) != 1:
        return None
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def encrypt_message(message, e, n):
    return [pow(ord(char), e, n) for char in message]

def decrypt_message(cipher_list, d, n):
    return ''.join([chr(pow(char, d, n)) for char in cipher_list])

def get_random_prime(bits):
    while True:
        num = random.randint(10**(bits-1), 10**bits - 1)
        if is_prime(num):
            return num

# ===== RSA Game GUI =====

class RSAGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 RSA Interactive Game")
        self.root.geometry("650x500")
        self.root.configure(bg="#f5f5f5")

        self.stage = 0
        self.start_time = 0
        self.p = self.q = self.n = self.phi_n = self.e = self.d = 0
        self.encrypted = []
        self.decrypted = ""
        self.message = ""
        self.level_bits = 2  # Easy by default

        self.build_welcome()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_welcome(self):
        self.clear_window()
        tk.Label(self.root, text="🎓 Welcome to the RSA Game!", font=("Poppins", 20, "bold"), bg="#f5f5f5").pack(pady=20)
        tk.Label(self.root, text="Select Difficulty Level", font=("Poppins", 14), bg="#f5f5f5").pack(pady=10)

        self.difficulty = tk.StringVar(value="Easy")
        options = ["Easy", "Medium", "Hard"]
        ttk.Combobox(self.root, textvariable=self.difficulty, values=options, state="readonly", width=20).pack(pady=10)

        tk.Button(self.root, text="Start Game", command=self.start_game, font=("Poppins", 12), bg="#4CAF50", fg="white", width=20).pack(pady=20)

    def start_game(self):
        level = self.difficulty.get()
        if level == "Easy":
            self.level_bits = 2
        elif level == "Medium":
            self.level_bits = 3
        else:
            self.level_bits = 4
        self.stage = 1
        self.start_time = time.time()
        self.build_stage1()

    def build_stage1(self):
        self.clear_window()
        tk.Label(self.root, text="🔢 Stage 1: Prime Number Selection", font=("Poppins", 16, "bold"), bg="#f5f5f5").pack(pady=10)

        tk.Label(self.root, text="Enter Prime Number p:", font=("Poppins", 12), bg="#f5f5f5").pack()
        self.p_entry = tk.Entry(self.root, font=("Courier", 12), width=25)
        self.p_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Prime Number q:", font=("Poppins", 12), bg="#f5f5f5").pack()
        self.q_entry = tk.Entry(self.root, font=("Courier", 12), width=25)
        self.q_entry.pack(pady=5)

        tk.Button(self.root, text="Next", command=self.process_stage1, font=("Poppins", 12), bg="#2196F3", fg="white", width=12).pack(pady=20)

    def process_stage1(self):
        try:
            p = int(self.p_entry.get())
            q = int(self.q_entry.get())
            if not is_prime(p) or not is_prime(q):
                raise ValueError("Both numbers must be prime!")
            self.p, self.q = p, q
            self.n = p * q
            self.phi_n = (p - 1) * (q - 1)
            self.build_stage2()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def build_stage2(self):
        self.clear_window()
        tk.Label(self.root, text="🔐 Stage 2: Key Generation", font=("Poppins", 16, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(self.root, text=f"n = {self.n}", font=("Poppins", 12), bg="#f5f5f5").pack()
        tk.Label(self.root, text=f"ϕ(n) = {self.phi_n}", font=("Poppins", 12), bg="#f5f5f5").pack(pady=10)

        self.e_list = generate_e(self.phi_n)
        self.e_var = tk.IntVar()
        self.e_var.set(self.e_list[0])
        tk.Label(self.root, text="Select Public Key Exponent (e):", font=("Poppins", 12), bg="#f5f5f5").pack()
        ttk.Combobox(self.root, textvariable=self.e_var, values=self.e_list, state="readonly", width=20).pack(pady=5)

        tk.Button(self.root, text="Generate Keys", command=self.process_stage2, font=("Poppins", 12), bg="#4CAF50", fg="white", width=16).pack(pady=20)

    def process_stage2(self):
        self.e = self.e_var.get()
        self.d = modinv(self.e, self.phi_n)
        if not self.d:
            messagebox.showerror("Error", "Failed to compute private key. Choose different e.")
        else:
            self.build_stage3()

    def build_stage3(self):
        self.clear_window()
        tk.Label(self.root, text="✉️ Stage 3: Encryption", font=("Poppins", 16, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(self.root, text=f"Public Key (n, e): ({self.n}, {self.e})", font=("Poppins", 12), bg="#f5f5f5").pack()

        tk.Label(self.root, text="Enter a message to encrypt:", font=("Poppins", 12), bg="#f5f5f5").pack(pady=5)
        self.message_entry = tk.Entry(self.root, font=("Courier", 12), width=50)
        self.message_entry.pack(pady=10)

        tk.Button(self.root, text="Encrypt", command=self.process_stage3, font=("Poppins", 12), bg="#2196F3", fg="white", width=12).pack(pady=10)

    def process_stage3(self):
        msg = self.message_entry.get()
        if not msg:
            messagebox.showwarning("Input Required", "Please enter a message.")
            return
        self.message = msg
        self.encrypted = encrypt_message(msg, self.e, self.n)
        self.build_stage4()

    def build_stage4(self):
        self.clear_window()
        tk.Label(self.root, text="🔓 Stage 4: Decryption", font=("Poppins", 16, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(self.root, text=f"Encrypted Message:\n{self.encrypted}", font=("Courier", 10), wraplength=600, bg="#f5f5f5").pack(pady=10)

        tk.Label(self.root, text="Enter your private key (d):", font=("Poppins", 12), bg="#f5f5f5").pack()
        self.d_entry = tk.Entry(self.root, font=("Courier", 12), width=30)
        self.d_entry.pack(pady=5)

        tk.Button(self.root, text="Decrypt", command=self.process_stage4, font=("Poppins", 12), bg="#4CAF50", fg="white", width=12).pack(pady=10)

    def process_stage4(self):
        try:
            d_input = int(self.d_entry.get())
            if d_input != self.d:
                raise ValueError("Incorrect private key!")
            decrypted = decrypt_message(self.encrypted, d_input, self.n)
            self.decrypted = decrypted
            self.show_result()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_result(self):
        self.clear_window()
        elapsed = round(time.time() - self.start_time, 2)

        tk.Label(self.root, text="🎉 Game Complete!", font=("Poppins", 18, "bold"), bg="#f5f5f5").pack(pady=15)
        tk.Label(self.root, text=f"Original Message: {self.message}", font=("Poppins", 12), bg="#f5f5f5").pack()
        tk.Label(self.root, text=f"Decrypted Message: {self.decrypted}", font=("Poppins", 12), bg="#f5f5f5").pack()
        tk.Label(self.root, text=f"Time Taken: {elapsed}s", font=("Poppins", 12, "italic"), bg="#f5f5f5").pack(pady=10)

        tk.Label(self.root, text="Enter your name for leaderboard:", font=("Poppins", 12), bg="#f5f5f5").pack()
        self.name_entry = tk.Entry(self.root, font=("Courier", 12), width=30)
        self.name_entry.pack(pady=5)

        tk.Button(self.root, text="Submit Score", command=lambda: self.save_score(elapsed), font=("Poppins", 12), bg="#9C27B0", fg="white", width=14).pack(pady=10)

    def save_score(self, elapsed):
        name = self.name_entry.get().strip()
        if name:
            with open("leaderboard.txt", "a") as f:
                f.write(f"{name},{elapsed}\n")
            self.show_leaderboard()
        else:
            messagebox.showwarning("Missing Name", "Please enter your name!")

    def show_leaderboard(self):
        self.clear_window()
        tk.Label(self.root, text="🏆 Leaderboard - Top 5", font=("Poppins", 16, "bold"), bg="#f5f5f5").pack(pady=15)

        try:
            with open("leaderboard.txt", "r") as f:
                scores = [line.strip().split(",") for line in f.readlines()]
                scores = sorted(scores, key=lambda x: float(x[1]))[:5]
        except:
            scores = []

        for i, (name, score) in enumerate(scores, 1):
            tk.Label(self.root, text=f"{i}. {name} - {score}s", font=("Poppins", 12), bg="#f5f5f5").pack()

        tk.Button(self.root, text="Play Again", command=self.build_welcome, font=("Poppins", 12), bg="#4CAF50", fg="white", width=14).pack(pady=20)

# Run App
root = tk.Tk()
app = RSAGame(root)
root.mainloop()
