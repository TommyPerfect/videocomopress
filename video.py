import ffmpeg, time

#gets Video- and Audio Bitrate of Video of desired Size
def getVideoAudioBitrate(path, targetSize, maxTime):
    minAudioBitrate = 32000
    maxAudioBitrate = 256000
    probe = ffmpeg.probe(path)
    # Video duration, in s.
    duration = min(float(probe['format']['duration']), maxTime)
    # Audio bitrate, in bps.
    tempcalc = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
    if tempcalc != None:
        audioBitrate = float(['bit_rate'])
    else:
        audioBitrate = float(0)
    # Target total bitrate, in bps.
    targetTotalBitrate = (targetSize * 1024 * 8) / (1.073741824 * duration)
    # Target audio bitrate, in bps
    if 10 * audioBitrate > targetTotalBitrate:
        audioBitrate = targetTotalBitrate / 10
        if audioBitrate < minAudioBitrate < targetTotalBitrate:
            audioBitrate = minAudioBitrate
        elif audioBitrate > maxAudioBitrate:
            audioBitrate = maxAudioBitrate
    # Target video bitrate, in bps.
    videoBitrate = targetTotalBitrate - audioBitrate
    return videoBitrate, audioBitrate

# compresses a video
def compress(videoPath, outputFileName, targetSize, maxTime, passes, cmd):
    maxTimeStr = time.strftime('%H:%M:%S', time.gmtime(maxTime))
    videoBitrate, audioBitrate = getVideoAudioBitrate(videoPath, targetSize, maxTime)
    i = ffmpeg.input(videoPath)
    ffmpeg.output(i, outputFileName,
        **{
            'c:v': 'libx265',
            'b:v': videoBitrate,
            'pass': passes,
            'c:a': 'aac',
            'b:a': audioBitrate,
            't': maxTimeStr,
        }
    ).overwrite_output().run(cmd)