# test_octal_quiz.py

import pytest
import hashlib

def load_quiz(filename="octal_quiz.txt"):
    """Beolvassa a kvízt a fájlból."""
    questions = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            question_line = lines[i].strip()
            answer = lines[i+1].strip()
            parts = question_line.split(" # ")
            question = parts[0]
            expected_checksum = parts[1] if len(parts) > 1 else None
            questions.append((question, answer, expected_checksum))
    return questions

def oct_to_dec(octal):
    """Oktális számot decimálisba vált."""
    return str(int(octal, 8))

def calculate_checksum(text):
    """Kiszámolja a szöveg SHA-256 checksumját"""
    return hashlib.sha256(text.encode()).hexdigest()[:8]

def validate_question(question, expected_answer, expected_checksum=None):
    """Ellenőrzi egyetlen kvízkérdést és választ."""
    calculated_checksum = calculate_checksum(question.strip())
    if expected_checksum and calculated_checksum != expected_checksum:
       return False, f"A kérdés checksumja érvénytelen: {question}. Elvárt checksum: {expected_checksum}, Kiszámított checksum: {calculated_checksum}"
    parts = question.split(' ')
    if "oktális szám decimális értéke" in question:
        try:
            octal = next((part for part in parts if part.isalnum() and all(c in '01234567' for c in part)), None)
            if octal is None:
                return False, f"Nem található oktális szám a kérdésben: {question}"
            calculated_answer = oct_to_dec(octal)
        except ValueError as e:
            return False, f"Érvénytelen oktális szám a kérdésben: {question}. Hibaüzenet: {e}"
        is_correct = calculated_answer == expected_answer
        return is_correct, f"Kérdés: {question}"
    else:
        return False, f"Ismeretlen kérdés formátum: {question}"

def create_test_functions():
    """Dinamikusan generál tesztfüggvényeket a kvízhez."""
    questions = load_quiz()
    for i, (question, expected_answer, expected_checksum) in enumerate(questions):
        test_name = f"test_question_{i+1}"
        def test_function(question=question, expected_answer=expected_answer, expected_checksum=expected_checksum):
            is_correct, message = validate_question(question, expected_answer, expected_checksum)
            assert is_correct, message
        test_function.__name__ = test_name
        globals()[test_name] = test_function

create_test_functions()
