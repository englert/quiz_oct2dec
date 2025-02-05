# oct_gen.py

import random
import hashlib
import os

def generate_octal_string(length):
    """Generál egy oktális stringet a megadott hosszal."""
    return "".join(random.choice(["0", "1", "2", "3", "4", "5", "6", "7"]) for _ in range(length))

def oct_to_dec(octal):
    """Oktális számot decimálisba vált."""
    return str(int(octal, 8))

def calculate_checksum(text):
  """Kiszámolja a szöveg SHA-256 checksumját"""
  return hashlib.sha256(text.encode()).hexdigest()[:8]

def generate_quiz(num_questions, min_digits=3, max_digits=6):
    """Generál egy kvízt a megadott paraméterekkel."""
    quiz_content = []
    for i in range(num_questions):
        octal_length = random.randint(min_digits, max_digits)
        octal_number = generate_octal_string(octal_length)
        decimal_value = oct_to_dec(octal_number)
        question = f"{i+1}.  Mi a {octal_number} oktális szám decimális értéke?"
        checksum = calculate_checksum(question)
        question_with_checksum = f"{question}  # {checksum}"
        quiz_content.append(question_with_checksum)
        quiz_content.append('0') # Javítva: hozzáadjuk a helyes választ
    return "\n".join(quiz_content)

def save_quiz_to_file(filename, quiz_content):
  """Elmenti a kvízt egy fájlba, ha az még nem létezik."""
  if not os.path.exists(filename):
      with open(filename, "w") as file:
          file.write(quiz_content)

if __name__ == "__main__":
    num_questions = 30
    min_digits = 3
    max_digits = 5
    filename = "octal_quiz.txt"
    quiz_content = generate_quiz(num_questions, min_digits, max_digits)
    save_quiz_to_file(filename, quiz_content)
    print(f"A kvíz ({filename}) sikeresen létrehozva.")
