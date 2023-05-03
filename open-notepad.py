# I cannot physically interact with the operating system as I am just a text-based AI 
# language model. However, I can provide you with a Python code that can perform the desired operations. 
# Here is a Python script that generates a random name, writes it to a text file, saves it, and opens it.

#```python
import random
import string
import os

# Generate a random file name
random_name = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.txt'

# Write the random name to a text file
with open(random_name, 'w') as f:
    f.write(random_name)

# Save the file
os.startfile(random_name)
#```

#This code uses the `random` and `string` modules to generate a random name. The name is created by concatenating 10 random lowercase letters and appending the ".txt" extension. The `open` function is used to write the name to a new text file and the `os.startfile` function is used to open the newly created file.

#Note: This script will only work on a Windows machine that has Notepad installed. If you are using a different operating system or text editor, you will need to modify the code accordingly.