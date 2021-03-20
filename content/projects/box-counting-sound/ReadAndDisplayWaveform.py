import numpy as np
import wave
import sys
import soundfile as sf
import matplotlib.pyplot as plt 
from scipy.fftpack import fft
from scipy.signal import blackman	
from random import gauss
from random import seed

def ReadAudioFile(audioFilePath):
    audioFilePath = r'Falls of Rauros - Patterns in Mythology - 02 Weapons of Refusal.mp3'
    data, samplerate = sf.read(audioFilePath)

def main():
    print ('this is my main')
    audioFilePath = r'C:\Users\krtzer\Documents\albino-grackle\content\projects\box-counting-sound\Falls of Rauros - Patterns in Mythology - 02 Weapons of Refusal.wav'
    data, samplerate = sf.read(audioFilePath)
    print (samplerate)
    print (len(data))

    noise = [gauss(0.0, 1.0) for i in range(len(data))]
    
    w = blackman(len(data))
    leftchannel = data[0:,0]
    rightchannel = data[0:,1]
    leftfft = fft(leftchannel*w)
    rightfft = fft(rightchannel*w)

    timeaxis = np.linspace(0.0, len(data)/samplerate, len(data))
    freqrange = np.linspace(0.0, samplerate/2, len(leftfft)//2)

    #make axis make sense 

    fig, axs = plt.subplots(2)
    fig.suptitle('Time Domain')
    axs[0].plot(timeaxis, leftchannel)
    axs[1].plot(timeaxis, rightchannel)

    # plt.show()

    fig2, axs2 = plt.subplots(2)
    fig2.suptitle('FFT')

    # // means floor division
    axs2[0].plot(freqrange, np.abs(rightfft[:len(rightfft)//2]))
    axs2[1].plot(freqrange, np.abs(leftfft[:len(leftfft)//2]))
    plt.show()

if __name__ == '__main__':
    main()