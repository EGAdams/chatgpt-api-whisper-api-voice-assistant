import os
import subprocess
import threading
import time
import datetime
import win32gui

NUMBER_OF_PROCESSES = 2

def open_notepad_file(file_name):
    subprocess.Popen(["notepad.exe", file_name])
    while True:
        window_handle = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if "Untitled - Notepad" in window_handle:
            win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Untitled - Notepad"))
            break
        # listen to the space bar press event
        win32gui.PumpWaitingMessages()
        
       # when the space bar is pressed, exit the loop
       
    
        
                
        time.sleep(1)

def create_file():
    random_name = "AI achieves breakthrough in natural language processing"
    today = datetime.datetime.now().strftime("%B_%d_%Y")
    user = os.getlogin()
    file_name = f"{random_name}__{today}.txt"
    with open(file_name, "w") as f:
        f.write(today + "\n")
        f.write(random_name + "\n\n")
        f.write(user + "\n\n\n")

if __name__ == "__main__":
    for i in range(NUMBER_OF_PROCESSES):
        t = threading.Thread(target=open_notepad_file, args=(f"temp{i}.txt",))
        t.start()

        create_file()
