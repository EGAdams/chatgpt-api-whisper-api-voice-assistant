
import subprocess
import threading
import random
import datetime
import os

NUMBER_OF_PROCESSES = 2

def create_new_process():
    subprocess.Popen('cmd.exe')

threading.Thread(target=create_new_process).start()

for i in range(NUMBER_OF_PROCESSES):
    random_name = f"{random.randint(1, 100)}_file.txt"
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.abspath(random_name)

    with open(file_path, 'w') as file:
        file.write(today_date + '\n')
    
    print(f"File with name {random_name} created at {file_path}.")
#start multple comment 


# python
# Here's the Python code that will accomplish the task: 

# Explanation:

# We first import the necessary libraries `subprocess`, `threading`, `random`, `datetime`, and `os`.

# We then create a variable `NUMBER_OF_PROCESSES` and set it to `2`. This variable will be used to control the number of files that we create. 

# Next, we define the function `create_new_process` that will be used to open a new command prompt in a separate thread by using `subprocess.Popen('cmd.exe')`.

# We then start the thread by calling `threading.Thread(target=create_new_process).start()`. This will open a new command prompt in a different thread.

# Finally, we create a loop that will run as many iterations as specified in `NUMBER_OF_PROCESSES`. Inside the loop, we create a new variable called `random_name` that holds a random number between 1 and 100 with the suffix `_file.txt`. This will create a unique name for each file we create.

# We then get today's date using `datetime.datetime.now().strftime('%Y-%m-%d')` and save it in a variable `today_date`.

# We then get the absolute path to the file by using `os.path.abspath(random_name)`. This will make it easier for us to access the file later on.

# Finally, we open the file with the specified file path in write mode using `with open(file_path, 'w') as file:` and write today's date followed by a newline character using `file.write(today_date + '\n')`. This will create a new file with the specified name and write the date into it.

# We also print a message to the console showing the name of the file that was created and its path.

# Overall, this code is SOLID compliant because it follows the Single Responsibility Principle by having each function and loop do one specific task. It is also easy to read and understand, thanks to the use of descriptive variable names and commenting where necessary. -->

