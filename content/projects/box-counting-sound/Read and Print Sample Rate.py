import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
fs, data = wavfile.read(r'C:\Program Files (x86)\Microsoft Office\root\Office16\MEDIA\APPLAUSE.WAV') # load the data
a = data.T[0] # this is a two channel soundtrack, I get the first track
# b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
c = fft(b) # calculate fourier transform (complex numbers list)
d = len(c)/2  # you only need half of the fft list (real signal symmetry)
plt.plot(abs(c[:(d-1)]),'r') 
plt.show()


#https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
#problems with git -> pathspec doesn't work with flac
# References
# https://stackoverflow.com/questions/45198277/pycharm-asks-me-if-i-want-to-add-idea-vcs-xml-to-git
# 
#data, samplerate = sf.read(r'C:\Program Files (x86)\Microsoft Office\root\Office16\MEDIA\APPLAUSE.WAV')
#print (samplerate)