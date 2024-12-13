import os, ffmpeg, sys, re,  video

cmd = ['ffmpeg', '-hwaccel','cuda', '-loglevel','quiet', '-stats']
wishedSize = 50
passes = 20
reduceiftoobig = 5
maxTime = 599.0


# für drag und drop und so
for param in sys.argv[1:]:
    droppedFile = param
    #print(droppedFile)
    size = wishedSize
    c = 0
    while True:
        newFile = re.sub('\\..*?$', '_small_' + str(int(size)) + '.mp4', droppedFile)
        print(newFile)
        video.compress(droppedFile, newFile, size * 1000, maxTime, passes, cmd)
        newSize = os.stat(newFile).st_size / (1024 * 1024)
        if newSize < wishedSize:
            break
        else:
            size *= (wishedSize/newSize)
            size -= (c * reduceiftoobig)
            c = c + 1
            print('File to big, doing again with ' + str(size) + ' wishedsize cause ' + str(newSize) + ' > ' + str(wishedSize) + ' !!!!!!')
 