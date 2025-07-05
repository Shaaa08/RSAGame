import random
import sympy
import time
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

# ======== UTILITY FUNCTIONS ========

def is_prime(n):
    return sympy.isprime(n)

def generate_prime(bits):
    """Generate a random prime in the range 2^(bits-1) to 2^bits"""
    return sympy.randprime(2 ** (bits - 1), 2 ** bits)

def get_user_prime(prompt, bits):
    while True:
        print(f"\n{prompt} Do you want to:")
        print("[1] Enter your own prime number")
        print("[2] Generate a random prime")
        choice = input("Choose (1/2): ").strip()
        if choice == '1':
            try:
                val = int(input("Enter your prime number: "))
                if is_prime(val):
                    return val
                else:
                    print("❌ That number is not prime. Try again.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
        elif choice == '2':
            val = generate_prime(bits)
            print(f"Generated prime: {val}")
            confirm = input("Do you want to use this prime? (y/n): ").strip().lower()
            if confirm == 'y':
                return val
        else:
            print("❌ Invalid input. Please choose 1 or 2.")

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Compute modular inverse of e mod phi"""
    return pow(e, -1, phi)

def ascii_encrypt(msg, e, n):
    """Encrypt message character by character"""
    return [pow(ord(char), e, n) for char in msg]

def ascii_decrypt(cipher, d, n):
    """Decrypt ciphertext back to plain text"""
    try:
        return ''.join([chr(pow(c, d, n)) for c in cipher])
    except:
        return "[ERROR: Failed to decrypt. Invalid characters.]"

# ======== LEADERBOARD FUNCTIONS ========

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    else:
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)

# ======== GAME FUNCTIONS ========

def get_difficulty():
    print("\nChoose your difficulty level:")
    print("[1] Easy (8-bit primes)")
    print("[2] Medium (16-bit primes)")
    print("[3] Hard (32-bit primes)")
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == '1':
            return 8
        elif choice == '2':
            return 16
        elif choice == '3':
            return 32
        else:
            print("❌ Invalid input. Please try again.")

def select_public_exponent(phi_n):
    candidates = [3, 5, 17, 257, 65537]
    valid = [e for e in candidates if gcd(e, phi_n) == 1]
    print(f"Choose a public exponent e from: {valid}")
    while True:
        try:
            e = int(input("Enter your choice for e: "))
            if e in valid:
                return e
            else:
                print("❌ Invalid. Must be one of the listed values.")
        except ValueError:
            print("❌ Please enter a valid integer.")

def rsa_game():
    print("\n=============================")
    print(" 🎮 Welcome to the RSA Game! 🎮")
    print("=============================")

    bits = get_difficulty()

    print("\n🔢 Stage 1: Prime Number Selection")
    print("⚠️  IMPORTANT: To ensure encryption works, choose primes so that p × q > 128.")
    print("💡 Tip: Pick large primes for stronger keys.")

    start_time = time.time()

    p = get_user_prime("First prime (p)", bits)
    q = get_user_prime("Second prime (q)", bits)
    print(f"\n✅ Selected primes: p = {p}, q = {q}")

    # Stage 2: Key Generation
    print("\n🔑 Stage 2: Key Generation")
    n = p * q
    phi_n = (p - 1) * (q - 1)

    if n < 128:
        print(f"❌ Your value of n = {n} is too small for ASCII message encryption.")
        print("🔁 Please restart the game and choose larger prime numbers.")
        return

    print(f"n = p * q = {n}")
    print(f"ϕ(n) = (p - 1)(q - 1) = {phi_n}")

    e = select_public_exponent(phi_n)
    d = mod_inverse(e, phi_n)

    print(f"\n✅ Public Key: (n = {n}, e = {e})")
    print(f"🔐 Private Key: (d = {d})")
    print(f"📌 Remember your private key for decryption later!")

    # Stage 3: Encryption
    print("\n🔒 Stage 3: Encryption")
    plaintext = input("Enter a message to encrypt: ")
    ciphertext = ascii_encrypt(plaintext, e, n)
    print("🔐 Encrypted Message:", ciphertext)

    # Stage 4: Decryption
    print("\n🔓 Stage 4: Decryption")
    try:
        try_d = int(input("Enter your private key (d): "))
        if try_d == d:
            decrypted = ascii_decrypt(ciphertext, try_d, n)
            print(f"✅ Decrypted Message: {decrypted}")
            if decrypted == plaintext:
                print("🎉 Success! The decrypted message matches the original.")
            else:
                print("⚠️ Warning: Decrypted message does not match exactly.")
        else:
            print("❌ Incorrect private key! Decryption failed.")
    except ValueError:
        print("❌ Invalid input. You must enter a number.")

    # Leaderboard
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    name = input("\nEnter your name for the leaderboard: ")

    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "time": total_time})
    leaderboard.sort(key=lambda x: x["time"])
    save_leaderboard(leaderboard)

    print("\n🏆 Leaderboard:")
    for i, entry in enumerate(leaderboard, start=1):
        print(f"{i}. {entry['name']} - {entry['time']} seconds")

# ======== MAIN LOOP ========

if __name__ == "__main__":
    while True:
        rsa_game()
        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != 'y':
            print("\nThanks for playing the RSA Game! Goodbye. 👋")
            break
