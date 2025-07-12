import subprocess, time, re, datetime

host = "www.google.com"


class myGlobals:
    connected = 1
    connectedWas = 0;
    timeLastConnected = time.time()
    firstrun = 1
    
mg = myGlobals()

def printLog(logstr):
    logstr = now.strftime("%Y-%m-%d %H:%M:%S") + " " + logstr
    with open("pings.txt", "a") as file:
        file.write(logstr + "\n")
        file.close()
    print (logstr)

def noConStart():
    if (mg.connected == 1):
        mg.connected = 0
        printLog("no connection start")
        mg.connectedWas = 0
            
            
def noConEnd():
    mg.connected = 1
    if (mg.connectedWas == 0):
        if (mg.firstrun == 0):
            printLog("Connected!! no connection for " + str(int(time.time() - mg.timeLastConnected)) + " Seconds")
        mg.connectedWas = 1
    mg.timeLastConnected = time.time()


while True:
    ping = subprocess.Popen(
        ["ping", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )    
    out, error = ping.communicate()
    result = out.split(b"\r\n")
    now = datetime.datetime.now()
    
    try:
        try:
            times = result[-2].decode().split()
            min = re.findall(r'\d+', times[2])[0]
            max = re.findall(r'\d+', times[5])[0]
            med = re.findall(r'\d+', times[8])[0]
            noConEnd()
            time.sleep(1)
        except ValueError:
            noConStart()
            time.sleep(1)
    except IndexError:
        noConStart()
        time.sleep(1)
        
    mg.firstrun = 0