import subprocess
import os
import datetime
import time
import threading

NUMBER_OF_PROCESSES = 2

def open_notepad():
    subprocess.Popen('notepad.exe')

def create_file():
    random_name = "AI_Significant_Event"
    event_summary = "OpenAI_GPT-3.5_Model_Releases"
    today = datetime.datetime.now().strftime('%B_%d_%Y')
    file_name = f"{random_name}__{today}.txt"
    with open(file_name, 'w') as f:
        f.write(today + '\n' + event_summary + '\n\n\n' + os.getlogin() + '\n\n\n\n')

def main():
    # open a new cmd.exe process in a new window
    threading.Thread(target=subprocess.Popen, args=('start cmd.exe /k',)).start()

    # open notepad windows
    for i in range(NUMBER_OF_PROCESSES):
        threading.Thread(target=open_notepad).start()
        time.sleep(1)

        # create and save a new file
        create_file()
        time.sleep(1)

    # switch focus to the first notepad window
    subprocess.Popen('taskkill /IM notepad.exe')
    subprocess.Popen('start /MAX notepad.exe')

if __name__ == '__main__':
    main()
