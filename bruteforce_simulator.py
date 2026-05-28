import hashlib
import itertools
import string
import time
from datetime import datetime

def get_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def dictionary_attack(target_hash, wordlist_file):
    print(f"\n[*] Starting Dictionary Attack...")
    print(f"[*] Wordlist: {wordlist_file}")
    start = time.time()
    count = 0
    try:
        with open(wordlist_file, "r") as f:
            for word in f:
                word = word.strip()
                count += 1
                if get_hash(word) == target_hash:
                    elapsed = time.time() - start
                    print(f"\n[+] PASSWORD CRACKED!")
                    print(f"[+] Password : {word}")
                    print(f"[+] Attempts : {count}")
                    print(f"[+] Time     : {elapsed:.2f} seconds")
                    return word
    except FileNotFoundError:
        print(f"[-] Wordlist not found: {wordlist_file}")
        return None
    elapsed = time.time() - start
    print(f"\n[-] Password not found in wordlist")
    print(f"[-] Attempts: {count} in {elapsed:.2f} seconds")
    return None

def bruteforce_attack(target_hash, max_length=4):
    print(f"\n[*] Starting Brute Force Attack...")
    print(f"[*] Max length: {max_length}")
    chars = string.ascii_lowercase + string.digits
    start = time.time()
    count = 0
    for length in range(1, max_length + 1):
        for combo in itertools.product(chars, repeat=length):
            word = ''.join(combo)
            count += 1
            if get_hash(word) == target_hash:
                elapsed = time.time() - start
                print(f"\n[+] PASSWORD CRACKED!")
                print(f"[+] Password : {word}")
                print(f"[+] Attempts : {count}")
                print(f"[+] Time     : {elapsed:.2f} seconds")
                return word
            if count % 50000 == 0:
                print(f"[*] Tried {count} combinations...")
    elapsed = time.time() - start
    print(f"\n[-] Password not cracked")
    print(f"[-] Total attempts: {count} in {elapsed:.2f}s")
    return None

def estimate_crack_time(password):
    chars = 0
    if any(c.islower() for c in password): chars += 26
    if any(c.isupper() for c in password): chars += 26
    if any(c.isdigit() for c in password): chars += 10
    if any(c in string.punctuation for c in password): chars += 32
    combinations = chars ** len(password)
    speed = 1000000
    seconds = combinations / speed
    if seconds < 60: return f"{seconds:.1f} seconds"
    elif seconds < 3600: return f"{seconds/60:.1f} minutes"
    elif seconds < 86400: return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000: return f"{seconds/86400:.1f} days"
    else: return f"{seconds/31536000:.1f} years"

print("\n" + "="*50)
print("  BRUTE FORCE SIMULATION MODULE")
print(f"  Date: {datetime.now()}")
print("="*50)

password = input("\nEnter password to test: ")
target_hash = get_hash(password)
print(f"\n[*] Target MD5 hash: {target_hash}")
print(f"[*] Estimated crack time: {estimate_crack_time(password)}")

print("\n[1] Dictionary Attack")
result = dictionary_attack(target_hash, "wordlist.txt")

if not result:
    print("\n[2] Brute Force Attack (max 4 chars)")
    result = bruteforce_attack(target_hash, max_length=4)

with open("bruteforce_report.txt", "w") as f:
    f.write(f"BRUTE FORCE SIMULATION REPORT\n")
    f.write(f"Date: {datetime.now()}\n")
    f.write(f"Target Hash: {target_hash}\n")
    f.write(f"Estimated Crack Time: {estimate_crack_time(password)}\n")
    f.write(f"Result: {'Cracked - ' + result if result else 'Not cracked'}\n")

print(f"\n[+] Report saved: bruteforce_report.txt")
