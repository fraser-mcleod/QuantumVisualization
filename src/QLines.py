
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


    def boundingBox(self, left: Fraction, right: Fraction, top: Fraction, bottom: Fraction):
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
        # boundedFace = Face(None, None)
        # unBoundedFace = Face(None, None)


        # add both half edges moving around counter-clockwise
        e1 = HalfEdge(v1, v4, None, True, None, None)
        e2 = HalfEdge(v4, v1, e1, False, None, None)
        v1.setIncEdge(e1)
        v4.setIncEdge(e2)
        e1.setTwin(e2)

        # self.unBoundedFace = unBoundedFace

        # bottom edge
        e3 = HalfEdge(v4, v3, None, True, None, e1)
        e1.setNext(e3)
        e4 = HalfEdge(v3, v4, e3, False, e2, None)
        e3.setTwin(e4)
        e2.setPrev(e4)

        # right edge
        e5 = HalfEdge(v3, v2, None, True, None, e3)
        e3.setNext(e5)
        e6 = HalfEdge(v2, v3, e5, False, e4, None)
        v3.setIncEdge(e5)
        v2.setIncEdge(e6)
        e5.setTwin(e6)
        e4.setPrev(e6)

        # top edge
        # e7 = HalfEdge(v2, v1, None, boundedFace, e1, e5)
        e7 = HalfEdge(v2, v1, None, True, e1, e5)
        e5.setNext(e7)
        e1.setPrev(e7)
        e8 = HalfEdge(v1, v2, e7, False, e6, e2)
        e7.setTwin(e8)
        e2.setNext(e8)
        e6.setPrev(e8)
        self.outsideEdge = e8

        # add edges and faces to record
        self.vertexRecord.extend([v1, v2, v3, v4])
        # self.faceRecord.extend([boundedFace, unBoundedFace])
        self.edgeRecord.extend([e1, e2, e3, e4, e5, e6, e7, e8])


    def addLine(self, line: Line):
        """Add line to the existing arrangement"""
        print(f"Add line: {line.toString()}")
        e1 = self.leftMostedge(line).twin()  # twin so that it is interior edge
        print(f"LME: {e1.toString()}")
        # find intersection between line and edge, then determine if we need to create a new vertex
        p1 = self.lineEdgeInt(line, e1)
        if p1 == e1.dest().coord():
            e1 = e1.next()  # want to be on 'left' side of vertex

        if p1 == e1.origin().coord():
            e1.origin().degree += 1
            v1 = e1.origin()
        else:
            # create a new vertex and split the edge
            v1 = Vertex(p1, e1)
            edgeSplit1 = HalfEdge(e1.origin(), v1, None, e1.incFace(), e1, e1.prev())
            edgeSplit2 = HalfEdge(v1, e1.origin(), edgeSplit1, e1.twin().incFace(), e1.twin().next(), e1.twin())
            edgeSplit1.setTwin(edgeSplit2)
            edgeSplit1.prev().setNext(edgeSplit1)
            edgeSplit2.next().setPrev(edgeSplit2)

            e1.setPrev(edgeSplit1)
            e1.setOrigin(v1)
            e1.twin().setDest(v1)
            e1.twin().setNext(edgeSplit2)



        # while e1 is on a bounded face
        while (e1.boundedFace() is None):
            # print(f"Bounded Face: \ne1 = {e1.origin().coord()}->{e1.dest().coord()}\ne1.twin() = {e1.twin().origin().coord()}->{e1.twin().dest().coord()}")
            e1 = self.faceSplit(e1, v1, line)
            v1 = e1.origin()





    def faceSplit(self, e1: HalfEdge, v1: Vertex, line: Line) -> HalfEdge:
        # traverse through edges of inc face until one of them intersects the line
        e2 = e1
        e2 = e2.next()  # otherwise the origin of e2 will intersect
        p2 = self.lineEdgeInt(line, e2)
        while p2 is None:
            e2 = e2.next()
            p2 = self.lineEdgeInt(line, e2)

        print(f"Line: {line.toString()}")
        print(f"e1: {e1.toString()}")
        print(f"e2: {e2.toString()}")


        # print(f"e2: {e2.toSring()}\ne2.twin(): {e2.twin().toSring()}")
        # print(f"e2.twin().prev(): {e2.twin().prev().toSring()}")
        # If p2 is a vertex already:
        if p2 == e2.dest().coord():
            # create new edges from p1 to p2, create anew face, and update references
            v2 = e2.dest()
            # newFace = Face(None, None)  # FIX LATER
            newEdge1 = HalfEdge(v2, v1, None, True, e1, e2)
            newEdge2 = HalfEdge(v1, v2, newEdge1, True, e2.next(), e1.prev())
            # newFace.setOutComp(newEdge2)
            newEdge1.setTwin(newEdge2)
            e2.next().setPrev(newEdge2)
            e2.setNext(newEdge1)
            e1.prev().setNext(newEdge2)
            e1.setPrev(newEdge1)

            # find the and return the correct edge of the next face:
            nextEdge = newEdge2.next()
            slope = Line(nextEdge.dest().coord(), nextEdge.origin().coord()).slope()
            nextEdge = nextEdge.twin().next()
            slopeTest = Line(nextEdge.dest().coord(), nextEdge.origin().coord()).slope()
            while (slope != slopeTest):
                nextEdge = nextEdge.twin().next()
                slopeTest = Line(nextEdge.dest().coord(), nextEdge.origin().coord()).slope()


            return nextEdge

        else:
            # Construct v2 and new edges
            v2 = Vertex(p2, None)
            newEdge1 = HalfEdge(v2, v1, None, True, None, None)
            newEdge2 = HalfEdge(v1, v2, newEdge1, True, None, None)
            newEdge1.setTwin(newEdge2)

            newEdge3 = HalfEdge(v2, e1.dest(), None, True, None, None)
            newEdge4 = HalfEdge(e2.dest(), v2, newEdge3, e2.twin().boundedFace(), None, None)
            newEdge3.setTwin(newEdge4)

            # Set the previous and next values for the new edges
            newEdge1.setNext(e1)
            newEdge1.setPrev(e2)

            newEdge2.setNext(newEdge3)
            newEdge2.setPrev(e1.prev())

            newEdge3.setNext(e2.next())
            newEdge3.setPrev(newEdge2)

            newEdge4.setNext(e2.twin())
            newEdge4.setPrev(e2.twin().prev())

            # Set the previous and next other affected edges
            e1.prev().setNext(newEdge2)
            e2.next().setPrev(newEdge3)
            e2.twin().prev().setNext(newEdge4)

            # set previous and next for e1 and e2 and their twins
            e2.setNext(newEdge1)
            e1.setPrev(newEdge1)
            e2.twin().setPrev(newEdge4)

            # fix dest origins of e2 and e2.twin
            e2.setDest(v2)
            e2.twin().setOrigin(v2)
            v2.setIncEdge(newEdge3)

            # create new face and update
            # f1 = e1.incFace()
            # f2 = Face(newEdge4, None)
            # newEdge1.setIncFace(f1)
            # newEdge2.setIncFace(f2)
            # newEdge3.setIncFace(f2)
            # newEdge4.setIncFace(e2.twin().incFace())

            return e2.twin()



    def lineEdgeInt(self, line: Line, edge: HalfEdge) -> tuple:
        """Determine if the given line and edge intersect"""
        l2 = Line(edge.origin().coord(), edge.dest().coord())
        p = line.intercept(l2)
        # print(p)
        if p == None:
            return None

        if (p[0] >= min(edge.origin().x(), edge.dest().x())) and (p[0] <= max(edge.origin().x(), edge.dest().x())) and (p[1] >= min(edge.origin().y(), edge.dest().y())) and (p[1] <= max(edge.origin().y(), edge.dest().y())):
            return p

        return None

    def leftMostedge(self, line: Line) -> HalfEdge:
        """Compute the edge of the bounding box that has the leftmost intersection with the given line"""
        # print(line.toString())
        leftMostIntersection = None
        leftMostEdge = None

        edge = self.outsideEdge
        startCoord = edge.origin().coord()

        while True:
            # print(edge.origin().coord())
            # is the edge vertical?
            intersection = self.lineEdgeInt(line, edge)
            # print(intersection)
            if intersection is not None:
                if leftMostIntersection is None:
                    leftMostIntersection = intersection
                    leftMostEdge = edge
                elif intersection[0] <= leftMostIntersection[0]:
                    leftMostIntersection = intersection
                    leftMostEdge = edge

            # move onto the next edge
            edge = edge.next()
            if edge.origin().coord() == startCoord:
                break

        # print("\nLME: ", leftMostEdge.toSring())
        # print("PREV: ", leftMostEdge.prev().toSring())
        # if the intersection is on the origin of a edge, return the previous edge instead
        if leftMostEdge.origin().coord() == leftMostIntersection:
            leftMostEdge = leftMostEdge.prev()


        return leftMostEdge






    def extremePoints(self) -> tuple[Fraction]:
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



# class Face:
#     """Simple face class

#     Attributes:
#         outComp: reference to half edge on the outer boundary of f, null if unbounded
#         inComp: reference to a half edge on the exterior of a face contained within an unbounded face
#     """

#     def __init__(self, outComp: HalfEdge, inComp: HalfEdge):
#         self._outComp = outComp
#         self._inComp = inComp

#     def outComp(self) -> HalfEdge:
#         return self._outComp

#     def setOutComp(self, newOutComp):
#         self._outComp = newOutComp

#     def inComp(self) -> HalfEdge:
#         return self._inComp

#     def setInComp(self, newInComp):
#         self._inComp = newInComp

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

    def __init__(self, origin, dest, twin, boundedFace: bool, next, prev):
        self._origin = origin
        self._dest = dest
        self._twin = twin
        self._BoundedFace = boundedFace
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


    def boundedFace(self) -> bool:
        return self._BoundedFace


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
        self._prev = new_prev

    def toString(self)->str:
        return f"{self.origin().coord()}->{self.dest().coord()}"






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
        self._p1 = p1
        self._p2 = p2
        self._yInt = None
        self._xInt = None
        # if the line is vertical
        if p2[0] == p1[0]:
            self._xInt = p2[0]
        else:
            self._slope = Fraction(p2[1]-p1[1],p2[0]-p1[0])
            self._yInt = Fraction(self._p1[1] - self._slope*p1[0])
            # if not horizontal
            if self._slope != Fraction(0, 1):
                self._xInt = Fraction(-self._yInt, self._slope)

        # if the line is not vertical
        if p2[0] != p1[0]:
            self._slope = Fraction(p2[1]-p1[1],p2[0]-p1[0])
            self._yInt = Fraction(self._p1[1] - self._slope*p1[0])
            # if the line is not horizontal
            if self._slope != 0:
                self._xInt = Fraction(self._yInt, (-self._slope))

        # if the line is vertical
        else:
            self._xInt = p1[0]
            self._slope = None




    def intercept(self, l: Line) -> tuple[Fraction]:
        """Return the intersetion between self and l. If parrallel return None
        """
        # print(self.toString())
        # print(l.toString())
        if l.isHorizontal():
            y = l.yInt()
            if self.isHorizontal():
                return None
            else:
                if self.isVertical():
                    x = self.xInt()
                    return (x, y)
                else:
                    x = Fraction(y - self.yInt(), self.slope())
        else:
            # print("l is not horizontal")
            if self.isHorizontal():
                # print("self is horizontal")
                y = self.yInt()
                if l.isVertical():
                    x = l.xInt()
                    return (x, y)
                else:
                    x = Fraction(y - l.yInt(), l.slope())
                    return (x, y)
            else:
                # neither of them are horizontal
                # print("self is not horizontal")
                if l.isVertical():
                    x = l.xInt()
                    if self.isVertical():
                        return None
                    else:
                        y = Fraction(self.slope()*x + self.yInt())
                else:
                    if self.isVertical():
                        x = self.xInt()
                        y = Fraction(l.slope()*x + l.yInt())
                    else:
                        # neither of them are vertical or horizontal
                        if l.slope() == self.slope():
                            return None
                        else:
                            x = Fraction(l.yInt() - self.yInt(), self.slope() - l.slope())
                            y = Fraction(self.slope()*x + self.yInt())
        return (x, y)



    def isVertical(self) -> bool:
        return self.yInt() is None

    def isHorizontal(self) -> bool:
        return self.xInt() is None

    # def horizontal(self) -> Fraction:
    #     return self._yInt

    # def vertical(self) -> Fraction:
    #     return self._xInt

    def x1(self) -> Fraction:
        return self._p1[0]

    def y1(self) -> Fraction:
        return self._p1[1]

    def x2(self) -> Fraction:
        return self._p2[0]

    def y2(self) -> Fraction:
        return self._p2[1]

    def slope(self) -> Fraction:
        return self._slope

    def yInt(self) -> Fraction:
        return self._yInt

    def xInt(self) -> Fraction:
        return self._xInt

    def toString(self) -> str:
        if self.isVertical():
            return f"x = {self.xInt()}"
        if self.isHorizontal():
            return f"y = {self.yInt()}"
        return f"y = {self.slope()}*x + {self.yInt()}"
