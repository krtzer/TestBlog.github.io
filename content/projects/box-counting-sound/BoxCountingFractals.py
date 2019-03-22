#goal for today: come up with a work flow to open audio files in Matlab
#Source: https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import soundfile as sf

data, samplerate = sf.read(r'C:\Users\krtzer\Documents\BlogWebSite\Python Playground\021000000.flac')
samplerate

spf = sf.read(r'C:\Users\krtzer\Documents\BlogWebSite\Python Playground\APPLAUSE.WAV','rb')

#spf = wave.open(r'C:\Users\krtzer\Documents\BlogWebSite\Python Playground\021000000.flac','rb')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
framerate = spf.getframerate()
# need to figure out how to what the bitness if of the signal 
# seems related to bitrate. This signal is 64 kbps
signal = np.fromstring(signal, 'int8')

#If Stereo
if spf.getnchannels() == 2:
    print ('Just mono files')
    sys.exit(0)

Time = np.linspace(0, len(signal)/framerate, num = len(signal))
	
plt.figure(1)
plt.title('Songs Waveform')
plt.plot(Time,signal)
plt.show()

def BoxCounting (signal):
	
	return fractalDimention