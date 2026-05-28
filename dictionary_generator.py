import itertools
import os
from datetime import datetime

def generate_wordlist(name, dob, output_file="wordlist.txt"):
    words = set()
    name = name.lower()
    dob = dob.replace("/", "").replace("-", "")

    # Basic combinations
    words.add(name)
    words.add(name + dob)
    words.add(name + dob[:4])
    words.add(name + dob[-4:])
    words.add(name.capitalize())
    words.add(name.capitalize() + dob)
    words.add(name + "123")
    words.add(name + "1234")
    words.add(name + "@123")
    words.add(name + "!")
    words.add(name + "2024")
    words.add(name + "2025")

    # Leet speak
    leet = name.replace("a","@").replace("e","3").replace("i","1").replace("o","0")
    words.add(leet)
    words.add(leet + dob[-4:])

    # Keyboard patterns
    words.update(["password","123456","qwerty","admin","letmein",
                  "welcome","monkey","dragon","master","123456789"])

    # Number mutations
    for n in range(1, 100):
        words.add(name + str(n))

    with open(output_file, "w") as f:
        for w in sorted(words):
            f.write(w + "\n")

    print(f"\n[+] Wordlist generated: {output_file}")
    print(f"[+] Total words: {len(words)}")
    print(f"[+] Time: {datetime.now()}")
    print("\nSample words:")
    for w in list(words)[:10]:
        print(f"  - {w}")

# Run it
name = input("Enter target name: ")
dob  = input("Enter date of birth (DDMMYYYY): ")
generate_wordlist(name, dob)
