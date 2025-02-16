import os, sys, video, re

def doDropped(sizeWished, timeMax = 599.0):

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
            v = video.video(pathInput, pathOutput, size, timeMax)
            
            v.compress()
            
            newSize = os.stat(pathOutput).st_size / (1024 * 1024)
            if newSize < sizeWished:
                break
            else:
                size *= (sizeWished/newSize)
                size -= (c * reduceiftoobig)
                c = c + 1
                print('File to big, doing again with ' + str(size) + ' sizeWished cause ' + str(newSize) + ' > ' + str(sizeWished) + ' !!!!!!')
     