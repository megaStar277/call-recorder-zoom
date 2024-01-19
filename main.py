from fastapi import FastAPI
import subprocess
import os
import time
from pydantic import BaseModel
import socket

app = FastAPI()

class ZoomMeeting(BaseModel):
    meeting_link: str

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

def find_open_port(starting_port):
    port = starting_port
    while True:
        if port_is_open(port):
            return port
        port += 1

def port_is_open(port, host='localhost'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5) # We don't want to wait forever
    # if the process using the port has not yet been closed at the operating system level 
    if not check_port_in_use(port):
        try:
            sock.bind((host, port))
            sock.listen(1)  # Listen for connections
            sock.close()
            return True
        except socket.error:  # If we can't open the port
            return False
    return False

def check_port_in_use(port):
    cmd = "sudo lsof -i :%s" % port
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if "LISTEN" in out.decode('utf-8'):
        return True
    else:
        return False

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/join-meeting")
def join_meeting(zoom_meeting: ZoomMeeting):
    port = find_open_port(5901)
    print(f"Joinding bot to {zoom_meeting.meeting_link}")
    print(f"First open port is {port}")
    command = f"sudo docker run -it \
    -v $(pwd)/recordings:/home/zoomrec/recordings \
    -v $(pwd)/logs:/home/zoomrec/logs:rw \
    -p {port}:5901 \
    --security-opt seccomp:unconfined \
    zoomrec:v0.1.0 \
    -u '{zoom_meeting.meeting_link}' \
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
    return contents