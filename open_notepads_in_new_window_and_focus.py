# Here's the Python code that will accomplish the task:

# ```python
import subprocess
import threading
import random
import datetime
import os

NUMBER_OF_PROCESSES = 2

def create_new_process():
    subprocess.Popen('start cmd.exe', shell=True)

threading.Thread(target=create_new_process).start()

notepad_processes = []

for i in range(NUMBER_OF_PROCESSES):
    random_name = f"{random.randint(1, 100)}_file.txt"
    today_date = datetime.datetime.now().strftime('%B %d, %Y')
    user_name = os.getlogin()

    subprocess.Popen(f'start notepad.exe /new-window {random_name}', shell=True)
    notepad_processes.append(random_name)

    with open(random_name, 'w') as file:
        file.write(today_date + '\n')
        file.write(user_name + '\n')
        file.write(random_name + '\n')

    new_file_name = f"{random_name}__{today_date}.txt"
    os.rename(random_name, new_file_name)

subprocess.Popen(f'taskkill /f /im notepad.exe', shell=True)

for notepad_process in notepad_processes:
    subprocess.Popen(f'start notepad.exe {notepad_process}', shell=True)

# ```

# Explanation:

# We first import the necessary libraries `subprocess`, `threading`, `random`, `datetime`, and `os`.

# We then create a variable `NUMBER_OF_PROCESSES` and set it to `2`. This variable will be used to control the number of files that we create.

# Next, we define the function `create_new_process` that will be used to open a new command prompt in a separate thread and a new window by using `subprocess.Popen('start cmd.exe', shell=True)`.

# We then start the thread by calling `threading.Thread(target=create_new_process).start()`. This will open a new command prompt in a different thread and a new window.

# We then create an empty list called `notepad_processes`, which we will use to store the names of the text files we open in Notepad.

# Finally, we create a loop that will run as many iterations as specified in `NUMBER_OF_PROCESSES`. Inside the loop, we create a new variable called `random_name` that holds a random number between 1 and 100 with the suffix `_file.txt`. This will create a unique name for each file we create.

# We then get today's date using `datetime.datetime.now().strftime('%B %d, %Y')` and save it in a variable `today_date`.

# We then get the user's name using `os.getlogin()` and save it in a variable `user_name`.

# Next, we open Notepad in a new window for each iteration by using `subprocess.Popen(f'start notepad.exe /new-window {random_name}', shell=True)` and store the name of the file being opened by appending `random_name` to the `notepad_processes` list.

# We then open the file with the specified file path in write mode using `with open(random_name, 'w') as file:` and write today's date, user's name, and random name into the file using `file.write(today_date + '\n')`, `file.write(user_name + '\n')`, and `file.write(random_name + '\n')`.

# We then rename the file to include the double underscore separator and today's date in September 04, 1972 format using `new_file_name = f"{random_name}__{today_date}.txt"` and `os.rename(random_name, new_file_name)`.

# After all files are created, we close all instances of Notepad using `subprocess.Popen(f'taskkill /f /im notepad.exe', shell=True)`.

# Finally, we loop through the `notepad_processes` list and reopen each file in the first window that was opened by using `subprocess.Popen(f'start notepad.exe {notepad_process}', shell=True)`.

# Overall, this code is SOLID compliant because it follows the Single Responsibility Principle by having each function and loop do one specific task. It is also easy to read and understand, thanks to the use of descriptive variable names and commenting where necessary.