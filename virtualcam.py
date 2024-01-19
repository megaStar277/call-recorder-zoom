import numpy as np
import pyvirtualcam

def run_cam():
    with pyvirtualcam.Camera(width=600, height=400, fps=20, device='/dev/video0') as cam:
        print(f'Using virtual camera: {cam.device}')
        frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        while True:
            frame[:] = (0, 0, 0)
            cam.send(frame)
            cam.sleep_until_next_frame()

run_cam()
