import re
import math
import string
from datetime import datetime

def analyze_password(password):
    score = 0
    feedback = []
    strength = ""

    length = len(password)
    has_lower  = bool(re.search(r'[a-z]', password))
    has_upper  = bool(re.search(r'[A-Z]', password))
    has_digit  = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    # Length scoring
    if length >= 16: score += 40
    elif length >= 12: score += 30
    elif length >= 8: score += 20
    elif length >= 6: score += 10
    else: score += 0; feedback.append("Too short — use at least 8 characters")

    # Complexity scoring
    if has_lower:  score += 10
    if has_upper:  score += 15; 
    if has_digit:  score += 15
    if has_symbol: score += 20

    # Entropy calculation
    charset = 0
    if has_lower:  charset += 26
    if has_upper:  charset += 26
    if has_digit:  charset += 10
    if has_symbol: charset += 32
    entropy = length * math.log2(charset) if charset else 0

    # Common password check
    common = ["password","123456","qwerty","admin","letmein",
              "welcome","monkey","dragon","master","123456789",
              "password123","abc123","iloveyou","sunshine"]
    if password.lower() in common:
        score = 0
        feedback.append("This is a commonly known password — change it immediately!")

    # Feedback
    if not has_upper:  feedback.append("Add uppercase letters (A-Z)")
    if not has_lower:  feedback.append("Add lowercase letters (a-z)")
    if not has_digit:  feedback.append("Add numbers (0-9)")
    if not has_symbol: feedback.append("Add symbols (!@#$%^&*)")
    if length < 12:    feedback.append("Make it longer — at least 12 characters")

    # Strength label
    if score >= 80:   strength = "VERY STRONG 🟢"
    elif score >= 60: strength = "STRONG 🟡"
    elif score >= 40: strength = "MODERATE 🟠"
    elif score >= 20: strength = "WEAK 🔴"
    else:             strength = "VERY WEAK ⛔"

    # Display
    print(f"\n{'='*50}")
    print(f"  PASSWORD STRENGTH ANALYZER")
    print(f"  Date: {datetime.now()}")
    print(f"{'='*50}")
    print(f"\n[PASSWORD]  : {'*' * len(password)}")
    print(f"[LENGTH]    : {length} characters")
    print(f"[SCORE]     : {score}/100")
    print(f"[STRENGTH]  : {strength}")
    print(f"[ENTROPY]   : {entropy:.1f} bits")
    print(f"\n[COMPLEXITY CHECK]")
    print(f"  Lowercase  : {'✅' if has_lower  else '❌'}")
    print(f"  Uppercase  : {'✅' if has_upper  else '❌'}")
    print(f"  Numbers    : {'✅' if has_digit  else '❌'}")
    print(f"  Symbols    : {'✅' if has_symbol else '❌'}")

    if feedback:
        print(f"\n[RECOMMENDATIONS]")
        for f in feedback:
            print(f"  ⚠ {f}")

    # Save report
    with open("strength_report.txt", "w") as f:
        f.write(f"PASSWORD STRENGTH REPORT\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Length: {length}\n")
        f.write(f"Score: {score}/100\n")
        f.write(f"Strength: {strength}\n")
        f.write(f"Entropy: {entropy:.1f} bits\n")
        f.write(f"Recommendations:\n")
        for fb in feedback:
            f.write(f"  - {fb}\n")
    print(f"\n[+] Report saved: strength_report.txt")

password = input("\nEnter password to analyze: ")
analyze_password(password)
