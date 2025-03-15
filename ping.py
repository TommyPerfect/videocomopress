import subprocess, time

host = "www.google.com"

while True:
    ping = subprocess.Popen(
        ["ping", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )    
    out, error = ping.communicate()
    result = out.split(b"\r\n")
    print (result[-2])
    #time.sleep(1)