import os, ffmpeg, time, sys, re
from better_ffmpeg_progress import FfmpegProcess

cmd = ['ffmpeg', '-hwaccel','cuda', '-loglevel','quiet', '-stats']


def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = min(float(probe['format']['duration']), 599.0)
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate
    
    #os.system('ffmpeg -i ' + video_full_path + ' -vcodec libvpx -acodec libvorbis ' + output_file_name)

    i = ffmpeg.input(video_full_path)
    #ffmpeg.output(i, os.devnull,
    #              **{'c:v': 'libx265', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
    #              ).overwrite_output().run()
    
    # das ding tuts
    ffmpeg.output(i, output_file_name,
        **{
            'c:v': 'libx265',
            'b:v': video_bitrate,
            'pass': 20,
            'c:a': 'aac',
            'b:a': audio_bitrate,
            't': '00:09:59',
        }
    ).overwrite_output().run(cmd)
                 
                 
#does it with nice status bar and percentage, but uses 10% cpu for it...
# process = FfmpegProcess([
    # "ffmpeg", "-y",
    # "-hwaccel", "cuda",
    # "-i", video_full_path, 
    # "-c:v", "libx265", 
    # "-b:v", str(video_bitrate), 
    # "-pass", str(20), 
    # "-c:a", "aac", 
    # "-b:a", str(audio_bitrate), 
    # "-t", "00:09:59", 
    # "-stats_period", "10",
    # output_file_name
# ])    
# # Use the run method to run the FFmpeg command.
# process.run(
    # progress_bar_description = "Converting to " + output_file_name
# )
    
#, 'v:f': 'scale=540:-1'               -hwaccel cuda
#    os.system('ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i '.video_full_path.' -c:v h264_nvenc -preset slow '.output_file_name)
    
wished_size = 50
reduceiftoobig = 5
c = 0

# für drag und drop und so
for param in sys.argv[1:]:
    droppedFile = param
    #print(droppedFile)
    size = wished_size
    while True:
        newFile = re.sub('\\..*?$', '_small_' + str(int(size)) + '.mp4', droppedFile)
        print(newFile)
        #time.sleep(1)
        compress_video(droppedFile, newFile, size * 1000)
        newsize = os.stat(newFile).st_size / (1024 * 1024)
        if newsize < wished_size:
            break
        else:
            size *= (wished_size/newsize)
            size -= (c * reduceiftoobig)
            c = c + 1
            print('File to big, doing again with ' + str(size) + ' wishedsize cause ' + str(newsize) + ' > ' + str(wished_size) + ' !!!!!!')
    