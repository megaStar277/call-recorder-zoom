import subprocess
from datetime import datetime
import time
import random
from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
  api_key=os.getenv('API_KEY'),  # this is also the default, it can be omitted
)

def check_invalid_meeting():
    import pyautogui
    try:
        pyautogui.locateCenterOnScreen("./img/invalid_meeting_id.png", confidence=0.8)
        return True
    except Exception as e:
        return False
    
def join_meeting(name):
    import pyautogui

    while True:
        try: 
            pyautogui.locateCenterOnScreen("./img/name_field_check.png", confidence= 0.8)
            time.sleep(random.uniform(1,2))
            pyautogui.write(name, interval=0.1)

            x, y = pyautogui.locateCenterOnScreen("./img/join.png", confidence= 0.8)
            time.sleep(random.uniform(1,2))
            pyautogui.click(x, y)
            break
        except Exception as e:
            if check_invalid_meeting():
                print("Invalid Meeting Link Provided")
                return 0
            else:
                time.sleep(0.1)
    print("Joined. Waiting to be admitted")

    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen("./img/join_with_computer_audio.png", confidence= 0.8)
            time.sleep(random.uniform(1,2))
            pyautogui.click(x, y)
            break
        except Exception as e:
            try:
                x, y = pyautogui.locateCenterOnScreen("./img/join_audio.png", confidence= 0.8)
                time.sleep(random.uniform(1,2))
                pyautogui.click(x, y)
            except:
                time.sleep(0.1)
    print("Joined the meeting, Recording now...")

    return True
        
def record_audio(filename):
    proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-f",
            "pulse",
            "-i",
            "ZoomRec.monitor",
            "-acodec",
            "libmp3lame",
            "-b:a",
            "128k",
            "-async",
            "1",
            "-vn",
            f"/home/zoomrec/recordings/{filename}",
        ],
    )

    check_meeting_ended()

    proc.terminate()
    proc.wait()

def check_meeting_ended():
    import pyautogui
    while True:
        try:
            pyautogui.locateCenterOnScreen("./img/end.png", confidence=0.8)
            return True
        except Exception as e:
            time.sleep(1)

def record_meeting(name, description):
    if join_meeting(name):
        audio_name = f"{description if description else 'zoom'}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        record_audio(f"{audio_name}.mp3")
        return audio_name
    else:
        return 0
    
def transcribe_meeting(audio_name):
    audio_file = AudioSegment.from_mp3(f"/home/zoomrec/recordings/{audio_name}.mp3")

    audio_length =  len(audio_file)
    print(audio_length)
    transcription = ''
    ten_minutes= 600 * 1000

    for last_snippet_time_stamp in range(0, audio_length, ten_minutes):
        snippet = audio_file[last_snippet_time_stamp: ten_minutes]
        snippet.export("audio_snippet.mp3", format="mp3")
        snippet_transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=open("audio_snippet.mp3", "rb"), 
                response_format="text"
            )
        transcription = transcription + snippet_transcription

    print(transcription)

    #Optional
    with open(f"/home/zoomrec/recordings/{audio_name}.txt", "w") as file:
        file.write(transcription)

# Setting logging
from loguru import logger
import sys

logfile = "./logs/run.log"
logger.add(logfile, format="{message}", level="INFO")

class StreamToLogger:
    def __init__(self, level="INFO"):
        self.level = level

    def write(self, message):
        if message.rstrip() != "":
            logger.opt(depth=1).log(self.level, message.rstrip())

    def flush(self):
        pass

sys.stdout = StreamToLogger(level="INFO")


if __name__ == "__main__":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    import os

    os.environ["PULSE_SINK"] = "ZoomRec"

    if not os.path.exists("/home/zoomrec/recordings"):
        os.mkdir("/home/zoomrec/recordings")

    if not os.path.exists("/home/zoomrec/logs"):
        os.mkdir("/home/zoomrec/logs")

    import argparse

    parser = argparse.ArgumentParser(
        description="Script to receive command line parameters"
    )

    parser.add_argument("-u", "--url", type=str, help="Meeting URL")
    parser.add_argument("-i", "--id", type=str, help="Meeting ID")
    parser.add_argument("-p", "--passcode", type=str, help="Meeting Passcode")
    parser.add_argument("-n", "--name", type=str, help="Display Name", required=True)
    parser.add_argument("-d", "--description", type=str, help="Description")

    args = parser.parse_args()

    if args.url:
        url = args.url
        print(url)
        zoom = subprocess.Popen(f'zoom --url="{url}"', stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL,
                                shell=True, preexec_fn=os.setsid)
    else:
        id = args.id
        passcode = args.passcode
        print(id, passcode)
        zoom = subprocess.Popen(f'zoom --url="zoommtg://zoom.us/join?confno={id}&pwd={passcode}"', stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL,
                                shell=True, preexec_fn=os.setsid)

    name = args.name
    description = args.description

    time.sleep(random.uniform(3, 5))

    audio_name = record_meeting(name, description)
    if audio_name != 0:
        while True:
            if os.path.exists(f"/home/zoomrec/recordings/{audio_name}.mp3"):
                print(f'File {audio_name}.mp3 has been found!')
                transcribe_meeting(audio_name)
                break  # Exit the loop
            else:
                print(f'Waiting for the file {audio_name}.mp3...')
                time.sleep(1)  # Wait for 1 second and check again
        

