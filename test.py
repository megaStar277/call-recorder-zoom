from fastapi import FastAPI
import subprocess
import os
import time
from pydantic import BaseModel


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
subprocess.Popen(command, shell=True)
print("Bot joined successfully")