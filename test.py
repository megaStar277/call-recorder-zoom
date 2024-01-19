from fastapi import FastAPI
import subprocess
import os
import time
from pydantic import BaseModel

def check_new_txt_file(directory, known_files):
    while True:
        files = os.listdir(directory)
        new_files = [f for f in files if f.endswith(".txt") and f not in known_files]

        if new_files:
            print('New txt File Found:', new_files)
            # Updating the known_files list
            known_files += new_files
            return new_files[0]
        time.sleep(1)  # wait for 1 second before rechecking the directory

meeting_link = "https://us05web.zoom.us/j/89890236727?pwd=gjipDtbRFqQapUEJYIvYVanWD6Somo.1"

print(f"Joinding bot to {meeting_link}")
command = f"sudo docker run -it \
-v $(pwd)/recordings:/home/zoomrec/recordings \
-v $(pwd)/logs:/home/zoomrec/logs:rw \
-p 5912:5901 \
--security-opt seccomp:unconfined \
zoomrec:v0.1.0 \
-u '{meeting_link}' \
-n 'Bot' \
-d 'Botjoined'"
# Here you would typically use something like the subprocess module to execute the command

# run the command
known_files = os.listdir('recordings')
subprocess.Popen(command, shell=True)
print("start process")

result = check_new_txt_file('recordings', known_files)
print("completed")
with open(f"recordings/{result}", "r") as file:
    # read the file
    contents = file.read()
