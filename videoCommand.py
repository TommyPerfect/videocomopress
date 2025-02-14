import video

def doDropped(sizeWished, timeMax = 10.0):

    # für drag und drop und so
    for param in sys.argv[1:]:
        pathImput = param
        #print(droppedFile)
        size = sizeWished
        c = 0
        while True:
            newFile = re.sub('\\..*?$', '_small_' + str(int(size)) + '.mp4', pathImput)
            print(newFile)
            video = new video(
                pathImput, 
                pathOutput, 
                size, 
                timeMax,
            )
            video.compress(pathImput, newFile, size * 1000, timeMax, passes, cmd)
            newSize = os.stat(newFile).st_size / (1024 * 1024)
            if newSize < sizeWished:
                break
            else:
                size *= (sizeWished/newSize)
                size -= (c * reduceiftoobig)
                c = c + 1
                print('File to big, doing again with ' + str(size) + ' sizeWished cause ' + str(newSize) + ' > ' + str(sizeWished) + ' !!!!!!')
     