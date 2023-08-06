from . import ifileinfo
import pandas as pd

class CsvFileInfo(ifileinfo.IFileInfo):
    """
        CsvFileInfo is good when there is no actual file, but an array;
        The array must be shaped in (n,c) where c is the number of channels;
    """
    def __init__(self, samples, samplerate):
        self._samples = samples
        self._samplerate = samplerate
        pass

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        self.close()

    def getSamples(self):
        return self._samples

    def getSamplerate(self):
        return self._samplerate
    
    def getNumberOfFrames(self):
        return len(self._samples)
    
    def getNumberOfChannels(self):
        try:
            numchannels = self._samples.shape[1]
        except IndexError as e:
            numchannels = 1
        return numchannels

    def getFilepath(self):
        raise NotImplementedError("Not avaliable in csvFileInfo")

    #WRITE
    def setSamples(self, samples, framerate = None):
        if (framerate == None):
            framerate = self.getSamplerate()
        self._samples = samples
        self._samplerate = framerate
        return
    
    def truncate(self, num_frames):
        self._samples = self._samples[:num_frames]
        return

    def addSamples(self, samples):
        self._samples.append(samples)
        return 

    def close(self):
        
        return