import hashlib
from passlib.hash import sha512_crypt
from datetime import datetime

def hash_password(password):
    results = {}
    results['MD5']          = hashlib.md5(password.encode()).hexdigest()
    results['SHA1']         = hashlib.sha1(password.encode()).hexdigest()
    results['SHA256']       = hashlib.sha256(password.encode()).hexdigest()
    results['SHA512']       = hashlib.sha512(password.encode()).hexdigest()
    results['LINUX_SHA512'] = sha512_crypt.hash(password)
    return results

def simulate_shadow_entry(username, password):
    linux_hash = sha512_crypt.hash(password)
    return f"{username}:{linux_hash}:19000:0:99999:7:::"

def extract_and_display(username, password):
    print(f"\n{'='*55}")
    print(f"  HASH EXTRACTION MODULE")
    print(f"  Date: {datetime.now()}")
    print(f"{'='*55}")
    print(f"\n[TARGET] Username: {username}")
    print(f"[TARGET] Password: {password}")
    print(f"\n[HASHES GENERATED]")

    hashes = hash_password(password)
    for algo, h in hashes.items():
        print(f"\n  [{algo}]")
        print(f"  {h}")

    print(f"\n[SIMULATED /etc/shadow ENTRY]")
    print(f"  {simulate_shadow_entry(username, password)}")

    print(f"\n[HASH ALGORITHM INFO]")
    print(f"  MD5     → Weak, broken, avoid")
    print(f"  SHA1    → Weak, deprecated")
    print(f"  SHA256  → Moderate, acceptable")
    print(f"  SHA512  → Strong, recommended")
    print(f"  LINUX   → SHA512-crypt, used in /etc/shadow")

    with open("hash_report.txt", "w") as f:
        f.write(f"HASH EXTRACTION REPORT\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Username: {username}\n")
        f.write(f"Password: {password}\n\n")
        for algo, h in hashes.items():
            f.write(f"{algo}: {h}\n")
        f.write(f"\nShadow Entry:\n")
        f.write(simulate_shadow_entry(username, password))
    print(f"\n[+] Report saved: hash_report.txt")

username = input("Enter username: ")
password = input("Enter password to hash: ")
extract_and_display(username, password)
