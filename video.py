import os, ffmpeg, sys, re, time

class video:
    
    def __init__(
            pathImput, 
            pathOutput, 
            sizeWished, 
            maxTime, 
            withAudio = 1, 
            passes = 20, 
            reduceiftoobig = 5, 
            minAudioBitrate = 32000, 
            maxAudioBitrate = 256000
        ):
            
        self.pathImput = pathImput
        self.pathOutput = pathOutput
        self.sizeWished = sizeWished
        self.maxTime = maxTime
        self.passes = passes
        self.cmd = ['ffmpeg', '-hwaccel','cuda', '-loglevel','quiet', '-stats']
        self.withAudio = withAudio
        self.minAudioBitrate = minAudioBitrate
        self.maxAudioBitrate = maxAudioBitrate
        self.speed = 1.0
        self.videoBitrate = 0.0
        self.audioBitrate = 0.0
        self.targetTotalBitrate = 0.0
        self.duration = 0.0
        self.durationWished = 0.0
        
    #gets Video- and Audio Bitrate of Video of desired Size
    def getVideoAudioBitrate():
        probe = ffmpeg.probe(self.pathImput)
        self.duration = float(probe['format']['duration'])
        speed = 1
        # Video duration, in s.
        self.durationWished = min(orgTime, self.maxTime)
        if orgTime > self.maxTime:
            speed = orgTime / self.maxTime
        # Audio bitrate, in bps.
        self.getAudioBitrate()
        # Target video bitrate, in bps.
        self.videoBitrate = targetTotalBitrate - self.audioBitrate

    # compresses a video
    def compress():
        maxTimeStr = time.strftime('%H:%M:%S', time.gmtime(maxTime))
        videoBitrate, audioBitrate, speed = self.getVideoAudioBitrate()
        i = ffmpeg.input(self.pathImput)
        ffmpeg.output(i, self.pathOutput,
            **{
                'c:v': 'libx265',
                'b:v': self.videoBitrate,
                'pass': self.passes,
                'c:a': 'aac',
                'b:a': self.audioBitrate,
                't': maxTimeStr,
                'filter:v': 'setpts=' + str(self.speed) + '*PTS'
            }
        ).overwrite_output().run(cmd)
    
    #gets Audio Bitrate GANZ unten, weils keiner mag!
    def getAudioBitrate():
        # Audio bitrate, in bps.
        hasAudio = self.withAudio ? next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None) : None
        if hasAudio != None or :
            self.audioBitrate = float(hasAudio['bit_rate'])
        else:
            self.audioBitrate = float(0)
        # Target total bitrate, in bps.
        self.targetTotalBitrate = (self.sizeWished * 1024 * 8) / (1.073741824 * self.duration)
        # Target audio bitrate, in bps
        if 10 * self.audioBitrate > self.targetTotalBitrate:
            self.audioBitrate = self.targetTotalBitrate / 10
            if self.audioBitrate < self.minAudioBitrate < self.targetTotalBitrate:
                self.audioBitrate = self.minAudioBitrate
            elif self.audioBitrate > self.maxAudioBitrate:
                self.audioBitrate = self.maxAudioBitrate