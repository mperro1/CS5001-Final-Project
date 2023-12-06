# Final Project Report

* Student Name: Marcela Perro
* Github Username: mperro1
* Semester: Fall 2023
* Course: CS5001



## Description 
- Overview: Password Strength and Guessing Time Analysis Using Python: The program attempts to guess passwords by generating a sequence of characters (using combinations of letters, numbers, and symbols) and compares them against a target password that a user inputs. 
- Objective:  To develop a Python-based tool that both generates passwords and estimates the time required to guess these passwords using common password cracking techniques.
- Relevance: Highlighting the importance of strong passwords in cybersecurity and how password complexity impacts guessing time.

## Key Features
### Use of the multiprocessing tool, and queues to cut runtime: 
- In python, multiprocessing refers to the ability of a program to run multiple processes simultaneously. Each process runs independently and can execute different parts of your code concurrently. 
- The role of a queue in multiprocesssing. As explained in the course videos, a queue is kind of a data structure that follows the FIFO principle. In the process of multiprocessing, a queue is used for communication and data exchange between different processes. 
- In the context of my brute_force_cracker.py script: When a worker process (running password_guess_worker) finds the correct password, it 'puts' this password into the queue.
The main process, which started all the worker processes, waits to 'get' the correct password from the queue. Once it receives the password, it can then terminate all processes, as the task is complete. 

## Guide
Download brute_force_cracker.py, password_generator.py open terminal and run example runs provided in this README file. 

## Code Review
### Methodoly:
1. Password Generation:
Python script generates passwords with varying complexity (including length, use of special characters, numbers, and case sensitivity). The purpose of this script is to generate random passwords for the user to get ideas to "crack" using the brute force cracker program. 

2. Password Guessing Simulation: Uses Python to simulate common password cracking techniques.
Incorporates timing mechanisms to measure the time taken to guess each password.

### Brute Force Approach: 
It uses a 'brute force' approach, which means it tries every possible combination of characters until it finds the correct password. This is like trying every key on a keyring to see which one opens a lock.
1. "password_guess_worker function" is designed to guess a password of a specified length. It's intended to run as a worker in a multiprocessing context, allowing multiple instances to operate in parallel for different password lengths.
```python
def password_guess_worker(target_password: str, characters: str, length, queue):
    for guess in itertools.product(characters, repeat=length):
        guessed_password = ''.join(guess)
        print(guessed_password)  # Add this line to print each guess
        if guessed_password == target_password:
            queue.put(guessed_password)
            return
```
Key Elements:
- Iterates through all combinations of given characters up to a specified length using itertools.product. Each combination is compared against the target password.
- If a match is found, it's placed in a multiprocessing queue and the function returns.
- Tracks and prints each guessed password, and the total number of attempts once the correct password is found.
- Usage in Multiprocessing: It's designed for efficiency in a multiprocessing setup, enabling parallel processing for faster execution.

2. "password_guesser function" is designed to work along the password_guess_worker function. Its purpose os tp guess a specified password using a brute force method. 
```python
def password_guesser(target_password: str):
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
```
Key Elements:
- Creates a pool of worker processes (password_guess_worker), each trying different combinations to guess the target password.
-Each worker process tries combinations of varying lengths, using ASCII letters, digits, and punctuation symbols. The function returns the guessed password as soon as it's found, and then terminates all processes.
- Guessing Process: The function tries combinations of these characters. It starts with combinations of length 1, then length 2, and so on, up to the length of the target password.
It uses two nested loops:
The outer loop (for length in range(1, len(target_password) + 1)) changes the length of the combinations.
The inner loop (for guess in itertools.product(characters, repeat=length)) creates every possible combination of the given length.
itertools.product is a special function that computes the Cartesian product, essentially pairing every element with every other element in the specified manner.
For each combination, the function joins the characters together (guessed_password = ''.join(guess)) to form a string.
It then checks if this string is the same as the target_password. If it is, the function stops and returns this guessed password. 
- The script is designed to work in a multiprocessing context, allowing multiple instances of the password_guess_worker function to run in parallel. This significantly speeds up the brute force process by simultaneously trying different combinations.
- As combinations are generated, each is compared against the target password. If a match is found, the guessed password is placed into a multiprocessing queue. This queue serves as a mechanism for communicating the successful guess back to the main process or thread.

3. "track_and_record_guess_time" function is designed to record the time taken to guess a password, providing performance metrics. 
```python
def track_and_record_guess_time(target_password: str):
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
```
Key Elements:
- The function records the current time before starting the password guessing process. This is the "start time" for the operation. The password_guesser function runs the brute force algorithm and returns the guessed password once it's found. 
- After the password is guessed, the function records the current time again. This is the "end time" for the operation. The function calculates the total time taken to guess the password by subtracting the start time from the end time. The function computes the average time taken to guess each character of the password. This is done by dividing the total time taken by the length of the target password. 
- Then function opens (or creates if it doesn't exist) the file opentimes.txt in append mode.
- It writes a line containing the target password, the total time taken to guess it, and the average time per character. 
- Finally, the function returns a tuple containing the guessed password, the total time taken to guess it, and the average time per character. This allows other parts of the program to access these results if needed.

### Major Challenges
The biggest challenge was figure out an efficient way to "crack" the passwords. Initially my program did not include multiprocessing tools, and every time I ran my program I would not be able to guess passwords longer than 3 characters. The multiprocessing tool allowed me to cut guessing time, and be able to test larger passwords. 
#### Initial version without multiprocessing: 
```python
def password_guesser(target_password):

    characters = string.ascii_letters + string.digits + string.punctuation

    # Iterate over different lengths of combinations
    for length in range(1, len(target_password) + 1):
        for guess in itertools.product(characters, repeat=length):
            guessed_password = ''.join(guess)
            if guessed_password == target_password:
                return guessed_password
```
This version was very slow. I had to manually stop my program from running because it would take over 20 minutes to crack a password with more than 3 characters. (see test runs)

### Password length vs password complexity: 
From my test runs, the length of password had longer runtime than password complexity (use of symbols). 

## Example Runs
### Example Run 1: Cracking a simple password 
Input:
```bash
python brute_force_cracker.py -gs "abc"
```
Expected output: 
```bash
Password guess is abc
Total Execution time: 0.3105583190917969 seconds
Average time per character: 0.10351943969726562 seconds
Average time per length: 0.05175971984863281 seconds
```
### Example Run 2: Cracking a more complex password 
Input: 
```bash
python brute_force_cracker.py -gs "P!!"
```
Expected output: 
```bash
Password guess is P!!
Total Execution time: 18.71308970451355 seconds
Average time per character: 6.237696568171184 seconds
Average time per length: 3.118848284085592 seconds
```
### Example Run 3: Cracking a password and inputting the length 
If length is not an integer value it will be disregarded. Program will focus on target_password as second argument always when action == guess
Input: 
```bash
 python brute_force_cracker.py --guess 'ab' '2'
```
Expected output:
```bash
Password guess is ab
Total Execution time: 0.1831216812133789 seconds
Average time per character: 0.09156084060668945 seconds
Average time per length: 0.06104056040445963 seconds
```
### Example Run 4: Failure to Crack Due to Length Limit
Input: 
```bash
 python brute_force_cracker.py -gs "VeryLongPassword123!"
```
Expected output: 
```bash
Ctrl + c "Keyboard interrupt. (Password will take forever!)
```
### Example Run 5: Generating a password 
Input 1:
```bash
  python brute_force_cracker.py -g '8'
```
Expected output:
```bash
Generated password= ABPq%hOO
```
Input 2: If length is not entered program will default to DEFAULT_LENGTH = 8 characters 
```bash
  python brute_force_cracker.py -g
```
Expected output:
```bash
Generated password= :}#i&nlP
```
### Example Run 6: Guessing a password and making sure runtime.txt file is generated with all the above runs 
Input:
```bash
python brute_force_cracker.py -gs "abc"
```
Expected Output:
Link to runtimes file 
### Example Run 7: Testing target_password with spaces 
Input: 
```bash
python brute_force_cracker.py -gs "a c"
```
```bash
Error: Target password should not contain spaces.
```

## Testing
brute_force_cracker_test_file.txt
## Missing Features / What's Next
### Optimization of Guessing/Cracking Algorithm:
- Dictionary Attack Integration: Before resorting to pure brute-force, use a dictionary of common passwords to attempt quicker matches.
- Command-Line Interface (CLI): Develop a more user-friendly CLI to allow users to specify options like password length, character set, and verbosity level.
- Progress Reporting: Implement a feature to report progress, such as the current number of attempts or the percentage of the search space covered.
- Pattern-Based Guessing: Implement pattern recognition to guess passwords based on common structures (e.g., "name + year").
## Final Reflection
My experience in this course has been both challenging and rewarding. The journey started with learning the basics of Python syntax and its core concepts, such as variables, data types, loops, and functions. One of the most exciting parts was diving into more advanced topics like file handling, error and exceptions, and especially multiprocessing, which opened my eyes to Python's capabilities in handling complex tasks efficiently. The final project was particularly enlightening. It not only consolidated my understanding of Python's syntax and logic but also introduced me to real-world applications of the language. Through this project, I learned how to manage multiple processes and the importance of efficient data handling between these processes using tools like multiprocessing queues. . This course has laid a strong foundation for my journey in Python programming, and I'm excited to explore its vast potential in the tech world.
