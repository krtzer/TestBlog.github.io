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

def CountBoxes (boxes, points):

    countedboxes = 0
    PointInBox = False
    for box in boxes[:]:
        for point in points[:]:
            if box.contains(point):
                PointInBox = True
                points.remove(point)
        if PointInBox:
            countedboxes +=1
            boxes.remove(box)
            PointInBox = False
    return countedboxes

data, samplerate = sf.read(r'C:\Users\krtzer\Documents\albino-grackle\content\projects\box-counting-sound\021000000.wav')

FirstXSamples = data[:300,0]

dataInPoints = []

for index, point in enumerate(FirstXSamples):
    	dataInPoints.append(Point(index,point))

# length of squre in samples
GridUnitLength = 2**21

# need to figure out how to what the bitness if of the signal 
# seems related to bitrate. This signal is 64 kbps

#last parmater 

Time = np.linspace(0, len(FirstXSamples)/samplerate, len(FirstXSamples))

xvertices = np.linspace(0, len(FirstXSamples), len(data)/GridUnitLength)
yvertices = np.linspace(-1, 1, len(data)/GridUnitLength)

hlines = [((x1, yi), (x2, yi)) for x1, x2 in zip(xvertices[:-1], xvertices[1:]) for yi in yvertices]
vlines = [((xi, y1), (xi, y2)) for y1, y2 in zip(yvertices[:-1], yvertices[1:]) for xi in xvertices]

intermeditateSum = MultiLineString(hlines + vlines)

grids = list(polygonize(intermeditateSum))

NumberofGrids = CountBoxes(grids, dataInPoints)

BLUE = '#6699cc'
SOMECOLOR = '#cc00cc'
fig = plt.figure(1)
ax = fig.gca()
#p = PatchCollection(grids, cmap=cm.jet, alpha=0.4)
#colors = 100*np.random.rand(len(grids))
#p.set_array(np.array(colors))
#ax.axis('scaled')

for grid in grids:
    	ax.add_patch(PolygonPatch(grid, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))

#for point in dataInPoints:
#		ax.add_patch(PolygonPatch(point, fc=SOMECOLOR, ec=SOMECOLOR, alpha=0.5, zorder=2))
plt.title('Songs Waveform')
plt.plot(FirstXSamples, 'bs')
plt.show()