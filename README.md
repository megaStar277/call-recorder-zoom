# Zoom Meeting Recorder🎥

## Run API endpoint

```shell
uvicorn main:app --reload
```

```shell
pip install -r requirements.txt
```

## Build Docker

```shell
$docker build . -t zoomrec:v1.0.0
```

## Run Docker

Give the mounted file the full permission

`````shell
chmod -R 777 $(pwd)/recordings
chmod -R 777 $(pwd)/logs
`````

- Running by url

```shell
docker run -it \\ 
  -v $(pwd)/recordings:/home/zoomrec/recordings \\
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\
  -p 5901:5901 \\
  --security-opt seccomp:unconfined \\
  zoomrec:v1.0.0 \\
  -u \<url\> \\
  -n \<name\> \\
  -d \<description_of_meeting\> \\
  -t 1 or 0 (if webinar: 1, normal meeting: 0) \\
  -m \<email\>
```

- Running by id/passcode

```shell
 docker run -it \\
  -v $(pwd)/recordings:/home/zoomrec/recordings \\
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\
  -p 5901:5901 \\ <br>
  --security-opt seccomp:unconfined \\
  zoomrec:v1.0.0 \\
  -i \<id\> \\ 
  -p \<passcode\> \\
  -n \<name\> \\
  -d \<description_of_meeting\> \\
  -t 1 or 0 (if webinar: 1, normal meeting: 0) \\
  -m \<email\>
```


## Run Docker with VCam

Run the virtual cam on the host machine

```shell
sudo modprobe -r v4l2loopback

sudo modprobe v4l2loopback devices=1 exclusive_caps=1

python3 virtualcam.py
```

Run the docker with device mounting

- Running by Url

```shell
docker run -it \\
  --device /dev/video0:/dev/video0 \\
  -v $(pwd)/recordings:/home/zoomrec/recordings \\
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\
  -p 5901:5901 \\
  --security-opt seccomp:unconfined \\
  zoomrec:v0.1.0 \\
  -u \<url\> \\
  -n \<name\> \\
  -d \<description_of_meeting\>
```

- Running by id/passcode

```shell
docker run -it \\
  --device /dev/video0:/dev/video0 \\
  -v $(pwd)/recordings:/home/zoomrec/recordings \\
  -v $(pwd)/logs:/home/zoomrec/logs:rw \\
  -p 5901:5901 \\
  --security-opt seccomp:unconfined \\
  zoomrec:v0.1.0 \\
  -i \<id\> \\ 
  -p \<passcode\> \\ 
  -n \<name\> \\
  -d \<description_of_meeting\>
```

## Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -am 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

This project is licensed under the [MIT License](https://poe.com/chat/LICENSE).

## Contact

For any questions or inquiries, please reach out to us at [ted563473@gmail.com](mailto:ted563473@gmail.com).
