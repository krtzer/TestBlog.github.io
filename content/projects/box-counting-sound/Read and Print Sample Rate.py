import soundfile as sf

#https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
#problems with git -> pathspec doesn't work with flac
# References
# https://stackoverflow.com/questions/45198277/pycharm-asks-me-if-i-want-to-add-idea-vcs-xml-to-git
#
data, samplerate = sf.read(r'C:\Users\krtzer\Documents\BlogWebSite\Python Playground\APPLAUSE.wav')
print (samplerate)