#!/bin/bash
set -e
echo 'Entrypoint is executing'
cleanup () {
    kill -s SIGTERM $!
    exit 0
}
trap cleanup SIGINT SIGTERM

VNC_IP=$(hostname -i)

# Change vnc password
mkdir -p "$HOME/.vnc"
PASSWD_PATH="$HOME/.vnc/passwd"

if [[ -f $PASSWD_PATH ]]; then
    rm -f "$PASSWD_PATH"
fi

echo "$VNC_PW" | vncpasswd -f >> "$PASSWD_PATH"
chmod 600 "$PASSWD_PATH"

# Remove old vnc locks
vncserver -kill "$DISPLAY" &> "$START_DIR"/vnc_startup.log || rm -rf /tmp/.X*-lock /tmp/.X11-unix &> "$START_DIR"/vnc_startup.log

echo -e "\nDISPLAY = $DISPLAY\nVNC_COL_DEPTH = $VNC_COL_DEPTH\nVNC_RESOLUTION = $VNC_RESOLUTION\nVNC_IP = $VNC_IP\nVNC_PORT = $VNC_PORT"
vncserver "$DISPLAY" -depth "$VNC_COL_DEPTH" -geometry "$VNC_RESOLUTION" &> "$START_DIR"/vnc_startup.log

echo -e "\nConnect to $VNC_IP:$VNC_PORT"

# Start xfce4
"$START_DIR"/xfce.sh &> "$START_DIR"/xfce.log

# Cleanup to ensure pulseaudio is stateless
rm -rf /var/run/pulse /var/lib/pulse /home/zoomrec/.config/pulse

# Start audio
pulseaudio -D --exit-idle-time=-1 --log-level=error

# Create speaker Dummy-Output
pactl load-module module-null-sink sink_name=ZoomRec sink_properties=device.description="speaker" > /dev/null
pactl set-source-volume ZoomRec.monitor 100%

# Create microphone Dummy-Output
pactl load-module module-null-sink sink_name=microphone sink_properties=device.description="microphone" > /dev/null
pactl set-source-volume microphone.monitor 100%

# Map microphone-Output to microphone-Input
pactl load-module module-loopback latency_msec=1 source=microphone.monitor sink=microphone > /dev/null
pactl load-module module-remap-source master=microphone.monitor source_name=microphone source_properties=device.description="microphone" > /dev/null
# Set microphone Volume
pactl set-source-volume 3 0%

echo -e "\nStart script.."
sleep 5

while getopts ":u:n:d:i:p:t:m:" flag; do
    case "${flag}" in
        u) url=${OPTARG};;
        n) name=${OPTARG};;
        d) description=${OPTARG};;
        i) id=${OPTARG};;
        p) passcode=${OPTARG};;
        t) type=${OPTARG};;
        m) mail=${OPTARG};;
    esac
done

echo $type

python3 ${HOME}/zoomrec.py -u "${url}" -n "${name}" -d "${description}" -i "${id}" -p "${passcode}" -t "${type}" -m "${mail}"