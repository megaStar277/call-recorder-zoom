import subprocess
from datetime import datetime
import time
import random
from urllib.parse import urlparse, urlunparse

class ZoomRecorder:

    def __init__(self, url, name, description, type, email=None):
        self.pyautogui = __import__('pyautogui')
        self.url = url
        self.name =name
        self.filename = f"{description if description else 'zoom'}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp3"
        self.email = email
        self.type = type
        
        # get id from url
        url_parts = urlparse(self.url).path.split('/')
        if '' in url_parts:
            url_parts.remove('')
        self.id = url_parts[-1]

    def check_invalid_meeting(self):
        try:
            self.pyautogui.locateCenterOnScreen("./img/invalid_meeting_id.png", confidence=0.8)
            return True
        except Exception as e:
            return False
    
    def check_in_webinar(self):
        try:
            self.pyautogui.locateCenterOnScreen("./img/leave.png", confidence= 0.8)
            return 1
        except Exception as e:
            return 0

    def join_webinar(self):
        
        time.sleep(2)
        # Join the meeting if the link is not working well
        while True:
            if self.check_waiting_room():
                break
            
            if self.check_in_webinar():
                return 1
            try:
                x, y = self.pyautogui.locateCenterOnScreen("./img/join_meeting.png", confidence= 0.8)
                self.pyautogui.click(x, y)
                time.sleep(random.uniform(1, 2))

                x, y = self.pyautogui.locateCenterOnScreen("./img/meeting_id.png", confidence= 0.8)
                self.pyautogui.click(x, y)
                time.sleep(random.uniform(0, 1))
                self.pyautogui.write(self.id, interval= 0.1)
                time.sleep(random.uniform(1, 2))

                x, y = self.pyautogui.locateCenterOnScreen("./img/name_field.png", confidence= 0.8)
                self.pyautogui.click(x, y)
                time.sleep(random.uniform(0, 1))
                self.pyautogui.write(self.name, interval= 0.1)
                time.sleep(random.uniform(1, 2))

                x, y = self.pyautogui.locateCenterOnScreen("./img/join.png", confidence= 0.8)
                self.pyautogui.click(x, y)
                time.sleep(random.uniform(1, 2))

                x, y = self.pyautogui.locateCenterOnScreen("./img/email_field.png", confidence= 0.8)
                self.pyautogui.click(x, y)
                time.sleep(random.uniform(0, 1))
                self.pyautogui.write(self.email, interval= 0.1)
                time.sleep(random.uniform(1, 2))

                x, y = self.pyautogui.locateCenterOnScreen("./img/join_webinar.png", confidence= 0.8)
                self.pyautogui.click(x, y)

            except Exception as e:
                print(e)

        print("Joining process success, waiting for starting")
        # waiting in the waiting room
        while True:
            if self.check_waiting_room() == 0:
                return 1
        
    def join_meeting(self):

        while True:
            try: 
                self.pyautogui.locateCenterOnScreen("./img/name_field_check.png", confidence= 0.8)
                time.sleep(random.uniform(1,2))
                self.pyautogui.write(self.name, interval=0.1)

                x, y = self.pyautogui.locateCenterOnScreen("./img/join.png", confidence= 0.8)
                time.sleep(random.uniform(1,2))
                self.pyautogui.click(x, y)
                break
            except Exception as e:
                if self.check_invalid_meeting():
                    print("Invalid Meeting Link Provided")
                    return 0
                else:
                    time.sleep(0.1)
        print("Joined. Waiting to be admitted")

        while True:
            try:
                x, y = self.pyautogui.locateCenterOnScreen("./img/join_with_computer_audio.png", confidence= 0.8)
                time.sleep(random.uniform(1,2))
                self.pyautogui.click(x, y)
                break
            except Exception as e:
                try:
                    x, y = self.pyautogui.locateCenterOnScreen("./img/join_audio.png", confidence= 0.8)
                    time.sleep(random.uniform(1,2))
                    self.pyautogui.click(x, y)
                except:
                    time.sleep(0.1)
        print("Joined the meeting, Recording now...")

        return True
            
    def record_audio(self):
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
                f"/home/zoomrec/recordings/{self.filename}",
            ],
        )

        self.check_meeting_ended()

        proc.terminate()
        proc.wait()

    def check_meeting_ended(self):
        while True:
            try:
                self.pyautogui.locateCenterOnScreen("./img/end.png", confidence=0.8)
                return True
            except Exception as e:
                time.sleep(1)

    def record_zoom(self):

        joined = self.join_webinar() if self.type == 1 else self.join_meeting()
        if joined:
            self.record_audio()
            return 1
        else:
            return 0

    def check_waiting_room(self):
        try:
            self.pyautogui.locateCenterOnScreen("./img/waiting_webinar.png", confidence= 0.8)
            return 1
        except Exception as e:
            pass
        try:
            self.pyautogui.locateCenterOnScreen("./img/waiting_soon.png", confidence= 0.8)
            return 1
        except Exception as e:
            pass
        return 0


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
    parser.add_argument("-t", "--type", type=int, help="if meeting -t 0 if webinar -t 1")
    parser.add_argument("-m", "--mail", type=str, help="email")

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
        url = f"zoommtg://zoom.us/join?action=join&confno={id}&pwd={passcode}"
        zoom = subprocess.Popen(f'zoom --url="{url}"', stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL,
                                shell=True, preexec_fn=os.setsid)

    name = args.name
    description = args.description
    zoom_type = args.type
    mail = args.mail

    time.sleep(random.uniform(3, 5))

    zoomrec = ZoomRecorder(url, name, description, zoom_type, mail)
    zoomrec.record_zoom()

