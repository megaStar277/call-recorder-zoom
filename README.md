## Build Docker

$ docker build . -t zoomrec:v1.0.0

## Run Docker

Give the mounted file the full permmision

$ chmod -R 777 $(pwd)/recordings

$ chmod -R 777 $(pwd)/logs 

- Running by url

$ docker run -it \\ <br>
  -v $(pwd)/recordings:/home/zoomrec/recordings \\ <br>
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\ <br>
  -p 5901:5901 \\ <br>
  --security-opt seccomp:unconfined \\ <br>
  zoomrec:v1.0.0 \\ <br>
  -u \<url\> \\ <br>
  -n \<name\> \\ <br>
  -d \<description_of_meeting\> \\ <br>
  -t 1 or 0 (if webinar: 1, normal meeting: 0) \\ <br>
  -m \<email\>

- Running by id/passcode

$ docker run -it \\ <br>
  -v $(pwd)/recordings:/home/zoomrec/recordings \\ <br>
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\ <br>
  -p 5901:5901 \\ <br>
  --security-opt seccomp:unconfined \\ <br>
  zoomrec:v1.0.0 \\ <br>
  -i \<id\> \\ <br>
  -p \<passcode\> \\ <br>
  -n \<name\> \\ <br>
  -d \<description_of_meeting\> \\ <br>
  -t 1 or 0 (if webinar: 1, normal meeting: 0) \\ <br>
  -m \<email\>


## Run Docker with VCam

Run the virtual cam on the host machine

$ sudo modprobe -r v4l2loopback

$ sudo modprobe v4l2loopback devices=1 exclusive_caps=1

$ python3 virtualcam.py

Run the docker with device mounting

- Running by url

$ docker run -it \\ <br>
  --device /dev/video0:/dev/video0 \\ <br>
  -v $(pwd)/recordings:/home/zoomrec/recordings \\ <br>
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\ <br>
  -p 5901:5901 \\ <br>
  --security-opt seccomp:unconfined \\ <br>
  zoomrec:v0.1.0 \\ <br>
  -u \<url\> \\ <br>
  -n \<name\> \\ <br>
  -d \<description_of_meeting\>

- Running by id/passcode

$ docker run -it \\ <br>
  --device /dev/video0:/dev/video0 \\ <br>
  -v $(pwd)/recordings:/home/zoomrec/recordings \\ <br>
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\ <br>
  -p 5901:5901 \\ <br>
  --security-opt seccomp:unconfined \\ <br>
  zoomrec:v0.1.0 \\ <br>
  -i \<id\> \\ <br>
  -p \<passcode\> \\ <br>
  -n \<name\> \\ <br>
  -d \<description_of_meeting\>

