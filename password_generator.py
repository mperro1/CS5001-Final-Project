"""
--------------------------
FINAL PROJECT
--------------------------
STUDENT: MARCELA PERRO
SEMESTER: FALL 2023
"""
import random
import string

def generate_password(length=12):
    """
    Generates a random password.

    This function creates a secure password by randomly selecting characters from a pool that incorporates
    uppercase and lowercase letters, digits, and special characters. The characters are shuffled
    before selection to enhance randomness.

    Args:
        length (int): The length of the password to be generated. Default is 12 characters.

    Returns:
        str: A string containing the randomly generated password.
    """
    # Characters to generate password from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Shuffling the characters
    shuffled = random.sample(characters, len(characters))

    # Generating password
    password = ''.join(random.choices(shuffled, k=length))

    return password
