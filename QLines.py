
from __future__ import annotations

from fractions import Fraction


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
        bbVertex: refernce to the top left vertex of the bounding box

    """
    def __init__(self, lines: list[Line]):
        self.lines = lines
        self.vertexRecord = []
        self.faceRecord = []
        self.edgeRecord = []
        self.unBoundedFace = None
        self.outsideEdge = None
        # create arrangement
        # left, right, top, bottom = self.findExtreme()
        # self.boundingBox(left, right, top, bottom)


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

        # TODO: vertex, edge, and face each need to be objects. That way we can actually store references to them
        #      not just to where they live in the list

        # add all four vertices and give reference to one of them with bounding box attribute
        v1 = Vertex((left, top), None)
        v2 = Vertex((right, top), None)
        v3 = Vertex((right, bottom), None)
        v4 = Vertex((left, bottom), None)
        self.bbVertex = v1


        # create two face objects - one bounded one unbounded
        boundedFace = Face(None, None)
        unBoundedFace = Face(None, None)


        # add both half edges moving around counter-clockwise
        e1 = HalfEdge(v1, v4, None, boundedFace, None, None)
        e2 = HalfEdge(v4, v1, e1, unBoundedFace, None, None)
        v1.setIncEdge(e1)
        v4.setIncEdge(e2)
        e1.setTwin(e2)
        boundedFace.setOutComp(e1)
        unBoundedFace.setInComp(e2)
        self.unBoundedFace = unBoundedFace
        self.outsideEdge = e1

        # bottom edge
        e3 = HalfEdge(v4, v3, None, boundedFace, None, e1)
        e1.setNext(e3)
        e4 = HalfEdge(v3, v4, e3, unBoundedFace, e2, None)
        e3.setTwin(e4)
        e2.setPrev(e4)

        # right edge
        e5 = HalfEdge(v3, v2, None, boundedFace, None, e3)
        e3.setNext(e5)
        e6 = HalfEdge(v2, v3, e5, unBoundedFace, e4, None)
        v3.setIncEdge(e5)
        v2.setIncEdge(e6)
        e5.setTwin(e6)
        e4.setPrev(e6)

        # top edge
        # e7 = HalfEdge(v2, v1, None, boundedFace, e1, e5)
        e7 = HalfEdge(v2, v1, None, boundedFace, e1, e5)
        e5.setNext(e7)
        e1.setPrev(e7)
        e8 = HalfEdge(v1, v2, e7, unBoundedFace, e6, e2)
        e7.setTwin(e8)
        e2.setNext(e8)
        e6.setPrev(e8)

        # add edges and faces to record
        self.vertexRecord.extend([v1, v2, v3, v4])
        self.faceRecord.extend([boundedFace, unBoundedFace])
        self.edgeRecord.extend([e1, e2, e3, e4, e5, e6, e7, e8])



    def lineArrangement(self):
        """Compute the arrangement of lines on the plane and store in DCEL

        Args:
            lines: a list of lines represented by a 4-tuple: (x1, y1, x2, y2) of two points on the line
        """
        assert self.bbVertex is not None  # make sure bounding box has been created

        for i, line in enumerate(self.lines):
            # find the edge to begin at
            e1 = self.leftMostedge(line).twin()
            # create a new vertex if it is not already one
            p1 = self.lineEdgeInt(line, e1)
            if (p1 == e1.origin().coord()):
                e1.origin().degree += 1  # may need to change this after
            else:
                # split edge e1 and create new vertex
                v = Vertex(p1, e1)
                newEdge1 = HalfEdge(e1.origin(), v, None, e1.incFace(), e1, e1.prev())
                newEdge2 = HalfEdge(v, e1.origin(), newEdge1, e1.twin().incFace(), e1.twin().next(), e1.twin())
                newEdge1.setTwin(newEdge2)
                e1.setOrigin(v)
                e1.setPrev(newEdge1)
                e1.twin().setDest(v)
                e1.twin().setNext(newEdge2)

            # while the face of e1 is bounded
            while (e1.incFace().outComp() is not None):
                # set the intersection point, face, and second intersection point
                p1 = e1.origin().coord()
                f1 = e1.incFace()
                e2 = e1.next()
                # find the next edge that intersects l
                while (self.lineEdgeInt(line, e2) is None):
                    e2 = e2.next()
                p2 = self.lineEdgeInt(line, e2)

                # normal means p2 is not a vertex
                e1 = self.simpleFaceSplit(e1, e2, f1, p1, p2)

                # if







    def simpleFaceSplit(self, e1: HalfEdge, e2: HalfEdge, f1: Face, p1: tuple, p2, tuple) -> HalfEdge:
        # In the first case, assume p1 is an existing vertex and p2 is a new vertex

        # We begin by p1, e1, and f. We walk counter-clockwise around f until we encounter
        # an edge that intersects line. Then set this point as p2 and this edge as e2.
        # We then need to create new vertices v1 nad v2, split e1 and e2 and update f.

        # Create new vertices, faces, and edges between the vertices
        v1 = Vertex(p1, None)
        if p2 != e2.dest().coord():
            v2 = Vertex(p2, None)
        else:
            v2 = e2.dest()

        newEdge1 = HalfEdge(v2, v1, None, f1, e1, None)  # Set twin and prev later
        newEdge2 = HalfEdge(v1, v2, newEdge1, None, None, e1.prev)  # Set face and next later
        newEdge1.setTwin(newEdge2)
        f1.setOutComp(newEdge1)
        f2 = Face(newEdge2, None)
        newEdge2.setIncFace(f2)

        if p2 != e2.dest.coord():
            # split e2 and update accordingly
            newEdge3 = HalfEdge(v2, e2.dest(), None, f2, e2.next(), newEdge2)  # set twin shortly
            newEdge4 = HalfEdge(e2.dest(), v2, newEdge3, e2.twin().incFace(), e2.twin(), e2.twin().prev())
            newEdge3.setTwin(newEdge4)

            e2.setDest(v2)
            e2.setNext(newEdge1)
            e2.twin().setOrigin(v2)
            e2.twin().setPrev(newEdge4)

            newEdge1.setPrev(e2)
            newEdge2.setNext(newEdge3)

            return e2.twin()
        else:
            e2.next().setPrev(newEdge2)
            newEdge2.setNext(e2.next())
            newEdge1.setPrev(e2)
            e2.setNext(newEdge1)

            # find the next face intersected by l
            # assume unique lines
            e2 = e2.next()
            slope1 = Fraction(e2.origin().coord[0]-e2.dest().coord[0], e2.origin().coord[1]-e2.dest().coord[1])
            e2 = e2.twin()
            e2 = e2.next()
            slope2 = Fraction(e2.origin().coord[0]-e2.dest().coord[0], e2.origin().coord[1]-e2.dest().coord[1])

            # walk around vertex until we find a line with equivalent slope, at which point we can return
            while(slope1 != slope2):
                e2 = e2.twin()
                e2 = e2.next()
                slope2 = Fraction(e2.origin().coord[0]-e2.dest().coord[0], e2.origin().coord[1]-e2.dest().coord[1])



            return e2


    def lineEdgeInt(self, line: Line, edge: HalfEdge):
        """Determine if the given line and edge intersect"""
        l2 = line(edge.origin.coord, edge.dest.coord)
        p = line.intercept(l2)
        if (p[0] >= min(edge.origin.coord[0], edge.dest.coord[0])) and (p[0] <= max(edge.origin.coord[0], edge.dest.coord[0])):
            return p

        return None

    def leftMostedge(self, line: Line) -> HalfEdge:
        """Compute the edge of the bounding box that has the leftmost intersection with the given line"""

        leftMostIntersection = None
        leftMostEdge = None
        # edge = self.unBoundedFace.outComp()  # may have to update list/single variable later
        edge = self.outsideEdge
        x = edge.origin().x()
        # is the edge vertical?
        if edge.origin().x() == edge.dest().coord().x():
            yInt = Fraction(line.slope*line.x2() + line.yInt())
            # does the intersection lie on the edge
            if (yInt <= edge.origin().y() and yInt >= edge.dest().y()) or (yInt >= edge.origin().y() and yInt <= edge.dest().y()):
                if (leftMostIntersection is not None):
                    if (edge.origin().x() < leftMostIntersection):
                        leftMostIntersection = edge.origin().x()
                        leftMostEdge = edge
        else:
            xInt = Fraction(edge.origin().x()-line.yInt, line.slope)
            # does the line intersect the edge
            if (xInt <= edge.origin().x() and xInt >= edge.dest().x()) or (xInt >= edge.origin().x() and xInt <= edge.dest().x()):
                if (leftMostIntersection is not None):
                    if (xInt < leftMostIntersection):
                        leftMostIntersection = xInt
                        leftMostEdge = edge

        # move onto the next edge
        edge = edge.next

        return leftMostEdge



    def extremePoints(self) -> tuple:
        """Find the leftmost, rightmost, topmost, and bottommost intersection point in self.lines

        return:
            a tuple (left, right, top, bottom) of integers representing the most extreme values
            of the intersection points
        """
        left, top = self.lines[0].intercept(self.lines[1])
        right, bottom = left, top

        for i in range(len(self.lines)-1):
            for j in range(i+1, len(self.lines)):
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

class Face:
    """Simple face class

    Attributes:
        outComp: reference to half edge on the outer boundary of f, null if unbounded
        inComp: reference to a half edge on the exterior of a face contained within an unbounded face
    """

    def __init__(self, outComp: HalfEdge, inComp: HalfEdge):
        self._outComp = outComp
        self._inComp = inComp

    def outComp(self) -> HalfEdge:
        return self._outComp

    def setOutComp(self, newOutComp):
        self._outComp = newOutComp

    def inComp(self) -> HalfEdge:
        return self._inComp

    def setInComp(self, newInComp):
        self._inComp = newInComp

class Vertex:
    """Simple Vertex class

    Attributes:
        coordinates: tuple (x, y)
        incidentEdge: reference to an arbitrary half edge with v as its origin
        degree: the degree of the vertex
    """

    def __init__(self, coord: tuple, incEdge: HalfEdge):
        self._coord = coord
        self._incEdge = incEdge
        self.degree = 2

    def x(self) -> float:
        return self._coord[0]

    def y(self) -> float:
        return self._coord[1]

    def incEdge(self) -> HalfEdge:
        return self._incEdge

    def setIncEdge(self, e: HalfEdge):
        self._incEdge = e

    def coord(self) -> tuple:
        return self._coord







class HalfEdge:
    """An undirected edge split into two half edges.

    The purpose of a half-edge is to have each edge correspond with a different face and make traversals easier.
    Each half edge has a twin half edge.

    Attributes:
        origin: reference to origin vertex
        dest: reference to dest vertex
        twin: reference to its twin half edge
        incFace: reference to the adjacent face
        next: the next edge along the face
        prev: the prev edge along the face
    """

    def __init__(self, origin, dest, twin, incFace, next, prev):
        self._origin = origin
        self._dest = dest
        self._twin = twin
        self._incFace = incFace
        self._next = next
        self._prev = prev


    def origin(self) -> Vertex:
        """Getter method for 'origin'."""
        return self._origin


    def setOrigin(self, new_origin: Vertex):
        """Setter method for 'origin'."""
        self._origin = new_origin


    def dest(self) -> Vertex:
        """Getter method for 'dest'."""
        return self._dest


    def setDest(self, new_dest: Vertex):
        """Setter method for 'dest'."""
        self._dest = new_dest


    def twin(self) -> HalfEdge:
        """Getter method for 'twin'."""
        return self._twin


    def setTwin(self, new_twin: HalfEdge):
        """Setter method for 'twin'."""
        self._twin = new_twin


    def incFace(self) -> Face:
        """Getter method for 'incFace'."""
        return self._incFace


    def setIncFace(self, new_incFace: Face):
        """Setter method for 'incFace'."""
        self._incFace = new_incFace


    def next(self) -> HalfEdge:
        """Getter method for 'next'."""
        return self._next


    def setNext(self, new_next: HalfEdge):
        """Setter method for 'next'."""
        self._next = new_next


    def prev(self) -> HalfEdge:
        """Getter method for 'prev'."""
        return self._prev


    def setPrev(self, new_prev: HalfEdge):
        """Setter method for 'prev'."""
        self.prev = new_prev






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
        self.slope = Fraction(p2[1]-p1[1],p2[0]-p1[0])
        self.yInt = Fraction(self.p1[1] - self.slope*p1[0])
        self.xInt = Fraction(self.yInt, (-self.slope))
        # print("y = ", self.slope, "*x + ", self.yInt)

    def intercept(self, l: Line) -> tuple:
        """Return the interscetion between self and l. If parrallel return None
        """
        if (self.slope == l.slope):
            return None

        x = (l.yInt - self.yInt)/(self.slope-l.slope)
        y = self.slope*x + self.yInt

        return (x, y)



    def x1(self) -> Fraction:
        return self.p1[0]

    def y1(self) -> Fraction:
        return self.p1[1]

    def x2(self) -> Fraction:
        return self.p2[0]

    def y2(self) -> Fraction:
        return self.p2[1]

    def slope(self) -> Fraction:
        return self.slope

    def yInt(self) -> Fraction:
        return self.yInt
