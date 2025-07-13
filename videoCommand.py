import os, sys, video, re, ffmpeg, subprocess

def doDropped(sizeWished, timeMax = 0, ensureFilesize = 1, useCuda = 1, reduceiftoobig = 7):
    print('sizeWished: ' + str(sizeWished) + ' timemax: ' + str(timeMax) + ' !!!!!!')
    # für drag und drop und so
    for param in sys.argv[1:]:
        pathInput = param
        print(pathInput)
        size = sizeWished
        c = 0
        while True:
            pathOutput = re.sub('\\..*?$', '_small_' + str(int(size)) + '.mp4', pathInput)
            print(pathOutput)
            v = video.video(pathInput, pathOutput, size, timeMax, useCuda)            
            v.compress()            
            newSize = os.stat(pathOutput).st_size / (1024 * 1024)
            if newSize < sizeWished or ensureFilesize == 0:
                break
            else:
                size *= (sizeWished/newSize)
                size -= (c * reduceiftoobig)
                c = c + 1
                print('File to big, doing again with ' + str(size) + ' sizeWished cause ' + str(newSize) + ' > ' + str(sizeWished) + ' !!!!!!')     
                
def convertDropped():
    cmd = ['ffmpeg', '-loglevel','quiet', '-stats']
    for param in sys.argv[1:]:
        pathInput = param
        print(pathInput)
        pathOutput = re.sub('\\..*?$', '.m4a', pathInput)
        print(pathOutput)
        cmd = ['ffmpeg', '-i', pathInput, '-vn', '-c:a', 'copy', pathOutput]
        print(cmd)
        subprocess.run(cmd) 