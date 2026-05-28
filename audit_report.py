import hashlib
import re
import math
import string
from datetime import datetime
from passlib.hash import sha512_crypt

def get_hash(p): return hashlib.md5(p.encode()).hexdigest()

def analyze_strength(password):
    score = 0
    has_lower  = bool(re.search(r'[a-z]', password))
    has_upper  = bool(re.search(r'[A-Z]', password))
    has_digit  = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    length = len(password)
    if length >= 16: score += 40
    elif length >= 12: score += 30
    elif length >= 8: score += 20
    elif length >= 6: score += 10
    if has_lower:  score += 10
    if has_upper:  score += 15
    if has_digit:  score += 15
    if has_symbol: score += 20
    charset = 0
    if has_lower:  charset += 26
    if has_upper:  charset += 26
    if has_digit:  charset += 10
    if has_symbol: charset += 32
    entropy = length * math.log2(charset) if charset else 0
    if score >= 80:   strength = "VERY STRONG"
    elif score >= 60: strength = "STRONG"
    elif score >= 40: strength = "MODERATE"
    elif score >= 20: strength = "WEAK"
    else:             strength = "VERY WEAK"
    return score, strength, entropy, has_lower, has_upper, has_digit, has_symbol

def crack_time(password):
    chars = 0
    if any(c.islower() for c in password): chars += 26
    if any(c.isupper() for c in password): chars += 26
    if any(c.isdigit() for c in password): chars += 10
    if any(c in string.punctuation for c in password): chars += 32
    combos = chars ** len(password)
    secs = combos / 1000000
    if secs < 60: return f"{secs:.1f} seconds"
    elif secs < 3600: return f"{secs/60:.1f} minutes"
    elif secs < 86400: return f"{secs/3600:.1f} hours"
    elif secs < 31536000: return f"{secs/86400:.1f} days"
    else: return f"{secs/31536000:.2f} years"

def dictionary_check(password):
    try:
        with open("wordlist.txt") as f:
            words = [w.strip() for w in f]
        return password in words
    except: return False

passwords = []
print("\n" + "="*55)
print("  PASSWORD SECURITY AUDIT REPORT GENERATOR")
print(f"  Date: {datetime.now()}")
print("="*55)
print("\nEnter passwords to audit (type 'done' when finished):")

while True:
    p = input("Password: ")
    if p.lower() == 'done': break
    passwords.append(p)

report = []
report.append("="*55)
report.append("  PASSWORD SECURITY AUDIT REPORT")
report.append(f"  Generated: {datetime.now()}")
report.append(f"  Total passwords audited: {len(passwords)}")
report.append("="*55)

weak_count = 0
strong_count = 0

for i, pwd in enumerate(passwords, 1):
    score, strength, entropy, hl, hu, hd, hs = analyze_strength(pwd)
    in_dict = dictionary_check(pwd)
    ct = crack_time(pwd)
    md5 = get_hash(pwd)
    linux = sha512_crypt.hash(pwd)

    if score < 40: weak_count += 1
    else: strong_count += 1

    print(f"\n[PASSWORD {i}] {'*'*len(pwd)}")
    print(f"  Score    : {score}/100 — {strength}")
    print(f"  Entropy  : {entropy:.1f} bits")
    print(f"  Crack time: {ct}")
    print(f"  In wordlist: {'YES ⚠ DANGER' if in_dict else 'No'}")
    print(f"  MD5 Hash : {md5}")

    block = [
        f"\n[PASSWORD {i}]",
        f"  Masked    : {'*'*len(pwd)}",
        f"  Score     : {score}/100 — {strength}",
        f"  Entropy   : {entropy:.1f} bits",
        f"  Crack Time: {ct}",
        f"  In Wordlist: {'YES — DANGER' if in_dict else 'No'}",
        f"  MD5 Hash  : {md5}",
        f"  Linux Hash: {linux}",
        f"  Lowercase : {'Yes' if hl else 'No'}",
        f"  Uppercase : {'Yes' if hu else 'No'}",
        f"  Numbers   : {'Yes' if hd else 'No'}",
        f"  Symbols   : {'Yes' if hs else 'No'}",
    ]
    report.extend(block)

report.append("\n" + "="*55)
report.append("  AUDIT SUMMARY")
report.append("="*55)
report.append(f"  Total Audited : {len(passwords)}")
report.append(f"  Weak/Very Weak: {weak_count}")
report.append(f"  Strong+       : {strong_count}")
report.append("\n  RECOMMENDATIONS:")
report.append("  - Use at least 12 characters")
report.append("  - Mix uppercase, lowercase, numbers and symbols")
report.append("  - Never use personal info like names or birthdays")
report.append("  - Never reuse passwords across accounts")
report.append("  - Use a password manager")
report.append("="*55)

with open("audit_report.txt", "w") as f:
    f.write('\n'.join(report))

print(f"\n{'='*55}")
print(f"  AUDIT SUMMARY")
print(f"  Weak passwords : {weak_count}")
print(f"  Strong passwords: {strong_count}")
print(f"[+] Full report saved: audit_report.txt")
