import socket
import subprocess

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

port = find_open_port(5902)
print(f"First open port is {port}")