from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
points = []
point1 = Point(0.5, 0.5)
point2 = Point(1.5, 1.5)
point3 = Point(2.5, 2.5)

points.append(point1)
points.append(point2)
points.append(point3)

boxes = []
polygon1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
polygon2 = Polygon([(0, 1), (1,1), (2,0), (2,1)])

boxes.append(polygon1)
boxes.append(polygon2)

def CountBoxes (boxes, points):
    countedboxes = 0
    PointInBox = False
    for box in boxes[:]:
        for point in points[:]:
            if box.contains(point):
                PointInBox = True
                #points.remove(point)
        if PointInBox:
            countedboxes +=1
            boxes.split(box)
            PointInBox = False


    return countedboxes

print CountBoxes()

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

