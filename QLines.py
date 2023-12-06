



class LineArrangement:
    """Represent an arrangement of lines in the plane.

    We choose to represent the subdivision created from lines using a doubly-connected edge list (DCEL).
    The purpose of this data structure is to represent a planar subdivision and efficiently:
        Traverse the boundary of a given face.
        Access one face from an adjacent one.
        Or visit all the edges of a given vertex.

    Attributes:
        lines: a list of lines in the plane.
        vertexRecord: a list of dictionaries to represent the vertices of the arrangement. Each dictionary will have:
                        coordinates: tuple (x, y)
                        incidentEdge: reference to an arbitrary half edge with v as its origin
        faceRecord: a list of disctionaries representing the faces of the arrangement. Each dict will have:
                        outComp: reference to half edge on the outer boundary of f, null if unbounded
                        inComp: reference to a half edge on a hole of a unbounded face
        edgeRecord: a list of dictionaries to represent the half edges of the arrangement. Each dict will have:
                        origin: the vertex origin
                        twin: its twin half-edge, chosen s.t. incident face lies to the left of given half edge
                        incidentFace: a lies to the left of edge e when traversed from origin destination.
                        next: next edge on the boundary of incident face
                        prev: previous edge on the boundary of incident face

    """
    def __init__(self, lines: list[Line]):
        self.lines = lines
        self.vertexRecord = []
        self.faceRecord = []
        self.edgeRecord = []
        # create arrangement

    def boundingBox(self, left: float, right: float, top: float, bottom: float):
        """Compute a bounding box with corners (left, top), (right, top), (right, bottom), (left, bottom)

        Args:
            left: leftmost value of the box
            right: rightmost value of the box
            top: topmost value of the box
            bottom: bottommost value of the box
        """
        # only want to compute bounding box if the arrangement is currently null
        assert len(self.vertexRecord) == 0

        # We will have 4 vertices, 8 half edges, and 2 faces
        self.vertexRecord.append({"self": 0, "coord": (left, top), "incEdge": 4})
        self.vertexRecord.append({"self": 1, "coord": (right, top), "incEdge": 5})
        self.vertexRecord.append({"self": 2, "coord": (right, bottom), "incEdge": 6})
        self.vertexRecord.append({"self": 3,"coord": (left, bottom), "incEdge": 7})

        # edges going counter clockwise, beginning at (left, top) vertex, left is bounded face
        self.edgeRecord.append({"self": 0, "origin": 0, "twin": 7, "incFace": 0, "next": 1, "prev": 3}) #0
        self.edgeRecord.append({"self": 1, "origin": 3, "twin": 6, "incFace": 0, "next": 2, "prev": 0}) #1
        self.edgeRecord.append({"self": 2, "origin": 2, "twin": 5, "incFace": 0, "next": 3, "prev": 1}) #2
        self.edgeRecord.append({"self": 3, "origin": 1, "twin": 4, "incFace": 0, "next": 0, "prev": 2}) #3

        # edges going clockwise, beginning at (left, top) vertex, left is unbounded face
        self.edgeRecord.append({"self": 4, "origin": 0, "twin": 3, "incFace": 1, "next": 5, "prev": 3}) #4
        self.edgeRecord.append({"self": 5, "origin": 1, "twin": 2, "incFace": 1, "next": 6, "prev": 4}) #5
        self.edgeRecord.append({"self": 6, "origin": 2, "twin": 1, "incFace": 1, "next": 7, "prev": 5}) #6
        self.edgeRecord.append({"self": 7, "origin": 3, "twin": 0, "incFace": 1, "next": 8, "prev": 6}) #7

        # 0 is the bounded face and 1 is the unbounded face
        self.faceRecord.append({"self": 0, "outComp": 4, "inComp": []})
        self.faceRecord.append({"self": 1, "outComp": None, "inComp:": [4]})

    def lineArrangement(self):
        """Compute the arrangement of lines on the plane and store in DCEL

        Args:
            lines: a list of lines represented by a 4-tuple: (x1, y1, x2, y2) of two points on the line
        """
        # begin by computing the bounding box


    def findExtreme(self) -> tuple:
        """Find the leftmost, rightmost, topmost, and bottommost intersection point in self.lines

        return:
            a tuple (left, right, top, bottom) of integers representing the most extreme values
            of the intersection points
        """
        left, top = self.lines[0].intercept(self.lines[1])
        right, bottom = left, top

        for i in range(len(self.lines)-1):
            for j in range(len, i+1, len(self.lines)):
                x, y = self.lines[i].intercept(self.lines[j])
                if (x < left):
                    left = x
                elif (x > right):
                    right = x

                if (y < bottom):
                    bottom = y
                elif (y > top):
                    top = y

        return (left, right, top, bottom)









class Line():
    """Represent a line

    Attributes:
        p1: an arbitrary point (x1, y1)
        p2: a second distinct arbitrary point (x2, y2)
        slope: the slope of the line
        xInt: the x-intercept
        yInt: the y-intercept
    """

    def __init__(self, p1: tuple, p2:tuple):
        self.p1 = p1
        self.p2 = p2
        self.slope = (p2[1]-p1[1])/(p2[1]-p2[0])
        self.yInt = self.p1[1] - self.slope*p1[0]
        self.xInt = self.yInt/(-self.slope)

    def intercept(self, l: Line) -> tuple:
        """Return the interscetion between self and l. If parrallel return None
        """
        if (self.slope == l.slope):
            return None

        x = (l.yInt - self.yInt)/(self.slope-l.slope)
        y = self.slope*x + self.yInt

        return (x, y)



    def x1(self):
        return self.p1[0]

    def y1(self):
        return self.p1[1]

    def x2(self):
        return self.p2[0]

    def y2(self):
        return self.p2[1]

    def slope(self):
        return self.slope

    def yInt(self):
        return self.yInt
