#goal for today: come up with a work flow to open audio files in Matlab
#Source: https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import soundfile as sf

data, samplerate = sf.read(r'C:\Users\krtzer\Documents\albino-grackle\content\projects\box-counting-sound\021000000.wav')

# need to figure out how to what the bitness if of the signal 
# seems related to bitrate. This signal is 64 kbps

Time = np.linspace(0, len(data)/samplerate, num = len(data))
	
plt.figure(1)
plt.title('Songs Waveform')
plt.plot(Time[0:3000000],data[0:3000000,0])
plt.show()

def BoxCounting (signal):
	
	return fractalDimention