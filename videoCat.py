import os, sys, video, re, time, subprocess

#def doDropped(sizeWished, timeMax = 0, useCuda = 1, reduceiftoobig = 7):
files = sys.argv[1:]
args = '|'.join(files)
#print(args + ' !!!!!!')
print(files)

#names = []
# für drag und drop und so
#for file in files:
#    names.append(os.path.basename(file))

files.sort()
    
namestr = '\'\nfile \''.join(files)
print(namestr)
namestr = 'file \'' + namestr + '\''

with open("filest.txt", "w") as f:
  f.write(namestr)


command = 'ffmpeg -f concat -safe 0 -i filest.txt -c copy outputn.mp4'

print('\n' + command + ' !!!!!!')
#time.sleep(10)
subprocess.run(command) 

#time.sleep(100)