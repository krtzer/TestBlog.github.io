#goal for today: come up with a work flow to open audio files in Matlab
#Source: https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import soundfile as sf
import matplotlib.cm as cm
from matplotlib import path
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon, MultiLineString
from shapely.ops import polygonize
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
from geopandas import GeoSeries

'''def MakeGrid (sideLength, audiodata song):
    	x1, x2, y1, y2 = 0
		for (y2 < 1): 
			for (x2 < len(song), )
		x1 = 0
		x2
		for (length(song))
		return fractalDimention
'''
data, samplerate = sf.read(r'C:\Users\krtzer\Documents\albino-grackle\content\projects\box-counting-sound\021000000.wav')

#dataInPoints = GeoSeries(map(Point, data[:300,:]))

dataInPoints = []

for x, y in data:
    	dataInPoints.append(Point(x,y))

# length of squre in samples
GridUnitLength = 2**21

# need to figure out how to what the bitness if of the signal 
# seems related to bitrate. This signal is 64 kbps

Time = np.linspace(0, len(data)/samplerate, len(data))

xvertices = np.linspace(0, len(data), len(data)/GridUnitLength)/samplerate
yvertices = np.linspace(-1, 1, len(data)/GridUnitLength)

#xvertices = [0,1,2,3]
#yvertices = [-2, -1,0,1,2]

#xx,yy = np.meshgrid(xvertices,yvertices)

hlines = [((x1, yi), (x2, yi)) for x1, x2 in zip(xvertices[:-1], xvertices[1:]) for yi in yvertices]
vlines = [((xi, y1), (xi, y2)) for y1, y2 in zip(yvertices[:-1], yvertices[1:]) for xi in xvertices]

intermeditateSum = MultiLineString(hlines + vlines)

grids = list(polygonize(intermeditateSum))

# Make grid ot match 
#xv,yv = np.meshgrid(np.linspace(0, len(data),100),Time)


# Copied from https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python 
first = -3
size  = (3-first)/100
xv,yv = np.meshgrid(np.linspace(-3,3,100),np.linspace(-3,3,100))
p = path.Path([(0,0), (0, 1), (1, 1), (1, 0)])  # square with legs length 1 and bottom left corner at the origin
flags = p.contains_points(np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis])))
grid = np.zeros((101,101),dtype='bool')
grid[((xv.flatten()-first)/size).astype('int'),((yv.flatten()-first)/size).astype('int')] = flags

xi,yi = np.random.randint(-300,300,100)/100,np.random.randint(-300,300,100)/100
vflag = grid[((xi-first)/size).astype('int'),((yi-first)/size).astype('int')]
plt.imshow(grid.T,origin='lower',interpolation='nearest',cmap='binary')
plt.scatter(((xi-first)/size).astype('int'),((yi-first)/size).astype('int'),c=vflag,cmap='Blues',s=90)
plt.show()
# End copied


BLUE = '#6699cc'
fig = plt.figure(1)
ax = fig.gca()
#p = PatchCollection(grids, cmap=cm.jet, alpha=0.4)
#colors = 100*np.random.rand(len(grids))
#p.set_array(np.array(colors))
#ax.axis('scaled')

for grid in grids:
    	ax.add_patch(PolygonPatch(grid, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))

for point in dataInPoints:
		ax.add_patch(PolygonPatch(point, fc='#cc00cc', ec='#cc00cc', alpha=0.5, zorder=2))
plt.title('Songs Waveform')
#plt.plot(Time[0:3000000],data[0:3000000,0])
plt.show()