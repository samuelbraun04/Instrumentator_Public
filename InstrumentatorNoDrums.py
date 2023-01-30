from os import listdir, remove
from platform import system
from pydub import AudioSegment
from pydub.silence import detect_leading_silence
from random import randint
from scipy.io import wavfile
from shutil import move, make_archive, copy
import dawdreamer as daw
import librosa

class NoDrumsGenerator():

    def __init__(self, DIRECTORY_PATH, SAMPLE_RATE=44100, BUFFER_SIZE=512):
        
        self.SAMPLE_RATE = SAMPLE_RATE
        self.BUFFER_SIZE = BUFFER_SIZE

        self.engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
        if system() == "Windows":
            self.conjoiner = "\\"
        else:
            self.conjoiner = "/"

        self.WORKSPACE_CONTAINER_PATH = DIRECTORY_PATH+self.conjoiner+'No Drums'+self.conjoiner+'Workspace'
        self.USED_SAMPLES_PATH = DIRECTORY_PATH+self.conjoiner+'No Drums'+self.conjoiner+'Samples'+self.conjoiner+'Used'
        self.NOT_USED_SAMPLES_PATH = DIRECTORY_PATH+self.conjoiner+'No Drums'+self.conjoiner+'Samples'+self.conjoiner+'Not Used'
        self.tagPath = DIRECTORY_PATH+self.conjoiner+'Ingredients'+self.conjoiner+'Samples'+self.conjoiner+'Tags'+self.conjoiner+'Tag.wav'
    
    def convertAudioFile(self, file_path, duration=None):
        sig, rate = librosa.load(file_path, duration=duration, mono=False, sr=self.SAMPLE_RATE)
        assert(rate == self.SAMPLE_RATE)
        return sig

    def chooseRandomFile(self, folder):
        files = listdir(folder)
        index = randint(0, len(files)-1)
        chosenFile = files[index]
        return chosenFile

    def run(self, template):
        
        #choose random sample
        chosenSample = self.chooseRandomFile(self.NOT_USED_SAMPLES_PATH)

        #get sample bpm
        bpm = int(chosenSample[chosenSample.rfind('-')+2:chosenSample.find('BPM')].strip())

        #set file up for splicing
        trim_leading_silence: AudioSegment = lambda x: x[detect_leading_silence(x) :]
        trim_trailing_silence: AudioSegment = lambda x: trim_leading_silence(x.reverse()).reverse()
        strip_silence: AudioSegment = lambda x: trim_trailing_silence(trim_leading_silence(x))
        unstrippedAudioSegment = AudioSegment.from_file(self.NOT_USED_SAMPLES_PATH+self.conjoiner+chosenSample)
        audioSegment = strip_silence(unstrippedAudioSegment)
        eightBarLength = (60*1000/bpm)*32.

        #splice files
        firstEightBars = audioSegment[0:eightBarLength]
        firstEightBars = firstEightBars.fade_out(duration=int((eightBarLength)/256))
        secondEightBars = audioSegment[eightBarLength:2*eightBarLength]
        secondEightBars = secondEightBars.fade_out(duration=int((eightBarLength)/256))
        firstEightBars.export(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'toEdit.wav', 'wav')

        #create high filtered splice
        playback_processor_1 = self.engine.make_playback_processor("playback_1", self.convertAudioFile(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'toEdit.wav'))
        filter_processor = self.engine.make_filter_processor("my_filter", 'high', 1000.0, 0.707107, 2.)
        graph1 = [
            (playback_processor_1, []),
            (filter_processor, ["playback_1"]),
        ]
        self.engine.load_graph(graph1)
        self.engine.render(32., beats=True)
        wavfile.write(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'high_filtered.wav', self.SAMPLE_RATE, (self.engine.get_audio()).transpose())
        highFiltered = AudioSegment.from_file(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'high_filtered.wav')
        highFiltered = highFiltered[0:eightBarLength]
        highFiltered = highFiltered + 4
        highFiltered = highFiltered.fade_out(duration=int((eightBarLength)/256))

        #create low filtered splice
        playback_processor_3 = self.engine.make_playback_processor("playback_3", self.convertAudioFile(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'toEdit.wav'))
        filter_processor_low = self.engine.make_filter_processor("my_filter", 'low', 250.0, 0.707107, 2.)
        graph3 = [
            (playback_processor_3, []),
            (filter_processor_low, ["playback_3"]),
        ]
        self.engine.load_graph(graph3)
        self.engine.render(32., beats=True)
        wavfile.write(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'low filtered.wav', self.SAMPLE_RATE, (self.engine.get_audio()).transpose())
        lowFiltered = AudioSegment.from_file(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'low filtered.wav')
        lowFiltered = lowFiltered[0:eightBarLength]
        lowFiltered = lowFiltered + 4
        lowFiltered = lowFiltered.fade_out(duration=int((eightBarLength)/256))

        #choose template
        if template == 1:
            finalAudio = firstEightBars+secondEightBars+firstEightBars+secondEightBars+lowFiltered+firstEightBars+secondEightBars+firstEightBars+secondEightBars
        if template == 2:
            finalAudio = firstEightBars+secondEightBars+firstEightBars+secondEightBars+highFiltered+firstEightBars+secondEightBars+firstEightBars+secondEightBars
        finalAudio = finalAudio + 1
        finalAudio.export(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'final untagged.wav', 'wav')

        #if all samples used, restart sample folder
        move(self.NOT_USED_SAMPLES_PATH+self.conjoiner+chosenSample, self.USED_SAMPLES_PATH+self.conjoiner+chosenSample)
        if len(listdir(self.NOT_USED_SAMPLES_PATH)) == 0:
            for file in listdir(self.USED_SAMPLES_PATH):
                move(self.USED_SAMPLES_PATH+self.conjoiner+file, self.NOT_USED_SAMPLES_PATH+self.conjoiner+file)
        
        #reset zip folder
        copy(self.USED_SAMPLES_PATH+self.conjoiner+chosenSample, self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'stems'+self.conjoiner+chosenSample)
        make_archive(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'stems_zipped', 'zip', self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'stems')
        remove(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'stems'+self.conjoiner+chosenSample)

        return self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'final untagged.wav', self.tagAudio(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'final untagged.wav'), self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'stems_zipped.zip', bpm

    def tagAudio(self, file):
    
        #add tag
        taggedBeatSegment = AudioSegment.from_file(file)
        tag = AudioSegment.from_file(self.tagPath)
        taggedBeatSegment = taggedBeatSegment.overlay(tag, loop=True)
        taggedBeatSegment.export(self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'final tagged.mp3', 'mp3')

        return self.WORKSPACE_CONTAINER_PATH+self.conjoiner+'final tagged.mp3'