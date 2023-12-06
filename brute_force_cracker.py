"""
Final Project    
=======================
Course:   CS 5001
Semester: FALL 2023
Student:  MARCELA PERRO

Brute force password cracker
"""
import sys
import random
import string
import itertools
from password_generator import generate_password
import multiprocessing
import time 


ACTION_GENERATE = "generate"
ACTION_GUESS = 'guess'
DEFAULT_LENGTH = "8"


def password_guess_worker(target_password: str, characters: str, length, queue):
    """
    Worker function for guessing a password of a specific length.

    This function iterates through all possible combinations of given characters up to a specified length
    and checks each combination against the target password. It is designed to be used as a worker in a
    multiprocessing context, where multiple instances of this function can run in parallel to cover different
    password lengths.

    Args:
        target_password (str): The password to be guessed.
        characters (str): A string containing all characters to be used in the guessing process.
        length (int): The specific length of password combinations to try.
        queue (multiprocessing.Queue): A queue to put the guessed password in once found.

    The function generates combinations using the itertools.product method, ensuring all possible combinations
    of the specified length are covered. If the guessed password matches the target password, it puts the
    guessed password into the provided queue and terminates.

    Note:
        This function prints each guessed password to the standard output, which can be useful for debugging
        but may slow down the execution if the output volume is large.
    """
    for guess in itertools.product(characters, repeat=length):
        guessed_password = ''.join(guess)
        print(guessed_password)  # Add this line to print each guess
        if guessed_password == target_password:
            queue.put(guessed_password)
            return


def password_guesser(target_password: str):
    """
    Attempts to guess a specified password using a brute-force approach.

    This function creates a pool of worker processes, each trying different combinations of characters
    to guess the target password. It employs multiprocessing to enhance the efficiency of the brute-force
    approach, splitting the guessing work across multiple processes.

    Args:
        target_password (str): The password that needs to be guessed.

    Returns:
        str: The guessed password that matches the target password.

    Each worker process tries combinations of different lengths, starting from a length of 1 up to the
    length of the target password. The function uses all ASCII letters (both uppercase and lowercase), 
    digits, and punctuation symbols as potential characters for the combinations.

    The function returns as soon as one of the worker processes successfully guesses the target password,
    and all processes are then terminated. If the target password is not within the considered character
    set or length, the function may not be able to guess the password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    queue = multiprocessing.Queue()

    # Create a pool of worker processes
    processes = []
    for length in range(1, len(target_password) + 1):
        process = multiprocessing.Process(target=password_guess_worker, args=(target_password, characters, length, queue))
        process.start()
        processes.append(process)

    # Wait for the first process to find the password
    guessed_password = queue.get()

    # Terminate all processes
    for process in processes:
        process.terminate()

    return guessed_password


def track_and_record_guess_time(target_password: str):
    """
    Tracks the time taken to guess a given password and records the performance metrics.

    This function attempts to guess the provided target password using the password_guesser function.
    It measures the time taken to successfully guess the password and calculates the average time 
    taken per character of the password. The performance data, including the total time taken and 
    the average time per character, is then appended to a file named 'opentimes.txt'.

    Args:
        target_password (str): The password to be guessed by the password_guesser function.

    Returns:
        tuple: A tuple containing the guessed password, total time taken to guess the password (in seconds),
               and the average time taken per character of the password (in seconds).

    The function appends each record in the 'opentimes.txt' file in the following format:
    "Password: [password], Time Taken: [total time]s, Average Time per Character: [average time]s\n"
    """
    start_time = time.time()
    guessed_password = password_guesser(target_password)
    end_time = time.time()

    time_taken = end_time - start_time
    password_length = len(target_password)
    avg_time_per_char = time_taken / password_length
    avg_time_per_length = time_taken / (password_length * (password_length + 1) / 2 ) #  Average time per length
    with open('runtimes.txt', 'a') as file:
        file.write(f"Password: {target_password}, Time Taken: {time_taken:.2f}s, Average Time per Character: {avg_time_per_char:.2f}s, Average Time per Length: {avg_time_per_length:.2f}s\n")

    return guessed_password, time_taken, avg_time_per_char, avg_time_per_length


def main(action: str, length: str = DEFAULT_LENGTH, target_password: str = None):
    """
    Main function to orchestrate password generation or guessing.

    This function serves as the primary entry point for the script. It determines whether to
    generate a new password or to guess an existing one based on the provided action. It uses
    the 'generate_password' function for generating passwords and 'password_guesser' for guessing.

    Args:
        action (str): Specifies the action to perform - 'generate' for generating a new password,
                      'guess' for guessing an existing password.
        length (str): The length of the password to be generated or the maximum length to be used
                      for guessing. It should be an integer or convertible to an integer.
        target_password (str): The password to be guessed. This is used only when the action is 'guess'.

    Returns:
        None: The function does not return anything but prints the generated or guessed password.
    """
    try:
        # Check to ensure target_password does not contain spaces
        if ' ' in target_password:
            raise ValueError("Target password should not contain spaces.")
    except ValueError as e:
        print("Error:", e)
        return 
    if action == '':
        print("You must enter a command. Available commands: guess, generate")
    elif action == ACTION_GENERATE:
        action = action.lower()
        if not length or length == '': 
            length = DEFAULT_LENGTH
        try:
            # Ensure length is an integer for 'generate' action
            length_int = int(length)
        except ValueError:
            print("Error: Length must be an integer for generating a password.")
            return
        generate_pass = generate_password(length_int)
        print(f"Generated password= {generate_pass}")
    elif action == ACTION_GUESS:
        if not target_password:
            print("Target password has not been provided")
        elif target_password == "":
            print("Target password has not been provided")
            try:
                length_int = int(length)
            except ValueError:
                print("Non-integer length entered. Ignoring length for guessing.")
                length_int = None
        else: 
            guessed_password, time_taken, avg_time_per_char, avg_time_per_length = track_and_record_guess_time(target_password)
            print(f"Password guess is {guessed_password}")
            print(f"Total Execution time: {time_taken} seconds")
            print(f"Average time per character: {avg_time_per_char} seconds")
            print(f"Average time per length: {avg_time_per_length} seconds")


if __name__ == "__main__":
    _action = ''
    _length = ''
    _target_password = ''
    if len(sys.argv) > 1:
        if sys.argv[1] == '-gs' or sys.argv[1] == '--guess':
            _action = ACTION_GUESS
            if len(sys.argv) > 2:
                _target_password = sys.argv[2]
            if len(sys.argv) > 3: 
                _length = sys.argv[3]
        elif sys.argv[1] == '-g' or sys.argv[1] == '--generate':
            _action = ACTION_GENERATE
            if len(sys.argv) > 2:
                _length = sys.argv[2]
                if len(sys.argv) > 3:
                    _target_password = sys.argv[3]

    main(_action, _length, _target_password)
