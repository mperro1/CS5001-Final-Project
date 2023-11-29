# Final Project Report

* Student Name: Marcela Perro
* Github Username: mperro1
* Semester: Fall 2023
* Course: CS5001



## Description 
General overview of the project, what you did, why you did it, etc. 
Password Strength and Guessing Time Analysis Using Python
- Objective:  To develop a Python-based tool that both generates passwords and estimates the time required to guess these passwords using common password cracking techniques.
- Relevance: Highlighting the importance of strong passwords in cybersecurity and how password complexity impacts guessing time.

Methodoly:
1. Password Generation:
Develop a Python script to generate passwords with varying complexity (including length, use of special characters, numbers, and case sensitivity).
Implement different algorithms for password generation (e.g., random, pattern-based, passphrase).

2. Password Guessing Simulation: Uses Python to simulate common password cracking techniques (brute force, dictionary attacks).
Incorporate timing mechanisms to measure the time taken to guess each password.
2 Brute Force Approach: 
- It uses a 'brute force' approach, which means it tries every possible combination of characters until it finds the correct password. This is like trying every key on a keyring to see which one opens a lock.
- Function Argument: target_password (str): This is the input to the function, the password that you want to guess. It's a string, which means it's made up of characters like letters and numbers.
- Character Set: characters = string.ascii_letters + string.digits + string.punctuation: Creates a list of characters to use for guessing the password. It includes: string.ascii_letters: All the letters in the alphabet, both uppercase and lowercase. string.digits: All the numbers from 0 to 9. string.punctuation: Symbols like !, @, #, etc.
- Guessing Process: The function tries combinations of these characters. It starts with combinations of length 1, then length 2, and so on, up to the length of the target password.
It uses two nested loops:
The outer loop (for length in range(1, len(target_password) + 1)) changes the length of the combinations.
The inner loop (for guess in itertools.product(characters, repeat=length)) creates every possible combination of the given length.
itertools.product is a special function that computes the Cartesian product, essentially pairing every element with every other element in the specified manner.
For each combination, the function joins the characters together (guessed_password = ''.join(guess)) to form a string.
It then checks if this string is the same as the target_password. If it is, the function stops and returns this guessed password. 

3. Data Collection and Analysis:


Collect data on password strengths and corresponding guessing times.
Analyze data to find correlations between password complexity and time required for guessing.
## Key Features
Highlight some key features of this project that you want to show off/talk about/focus on. 

## Guide
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features. 


## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 

### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.