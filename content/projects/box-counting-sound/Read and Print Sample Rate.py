import soundfile as sf

#https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
#problems with git -> pathspec doesn't work with flac

data, samplerate = sf.read(r'C:\Users\krtzer\Documents\BlogWebSite\Python Playground\APPLAUSE.wav')
print (samplerate)