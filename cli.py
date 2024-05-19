from video_manager import video_manager
from filtering_manager import filtering_manager
from audio_manager import audio_manager
import moviepy.editor as mp
import os


class NudityCensorCli:
    def __init__(self, path):
        self.path = path
        self.run_filter()
        self.applyExtraFilter()
        # random name
        rand = "random"
        audioName = "{}.mp3".format(rand)
        videoName = "{}.mp4".format(rand)

        self.saveFilteredVideo(videoName)
        self.saveFilteredAudio(audioName)

        self.mergeAudioVideo(videoName, audioName, "final.mp4")

        os.remove(audioName)
        os.remove(videoName)
        print("Done")


    def run_filter(self):
        vm = video_manager(self.path)
        fm = filtering_manager(vm, 22)
        thread = fm.startSyncThread()
        thread.join()
        self.secondsFilter = fm.state

    def saveFilteredVideo(self, path):
        vm = video_manager(self.path)
        fm = filtering_manager(vm, 22)
        fm.return_filtered_frames(self.secondsFilter, path)

    def mergeAudioVideo(self, videoPath, audioPath, path):
        audio = mp.AudioFileClip(audioPath)
        video1 = mp.VideoFileClip(videoPath)
        final = video1.set_audio(audio)
        final.write_videofile(path,codec= 'mpeg4' ,audio_codec='libvorbis')
    
    def saveFilteredAudio(self, path):
        am = audio_manager(self.path, lambda x: True)
        am.filter(self.secondsFilter)
        am.export(path)

    def applyExtraFilter(self):
        for index, value in enumerate(self.secondsFilter):
            if value == False:
                startBlur = index - 5
                endBlur = index
                if startBlur < 0:
                    startBlur = 0
                self.secondsFilter[startBlur:endBlur] = [False] * (endBlur - startBlur)
    

NudityCensorCli("C:/Users/ibrah/Downloads/GameofThrones-01x01-Clarke-HD-01_hd.mp4")
