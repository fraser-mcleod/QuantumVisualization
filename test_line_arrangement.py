import unittest

from src.LineArrangement import *

class TestLine(unittest.TestCase):
    def setUp(self):
            self.l1 = Line((0, 0), (1, 1))
            self.l2 = Line((0, -5), (1, 5))
            self.l3 = Line((Fraction(39, 4), 0), (0, 13))
            self.l4 = Line((10, 5), (20, 5))
            self.l5 = Line((13, 0), (13, 100))
            self.l6 = Line((1, 0), (10, 15))
            self.l7 = Line((6, 7), (8, 8))
            self.l8 = Line((14, 0), (11, 6))
            self.l9 = Line((6, 4), (0, 0))

            self.lineSet1 = [self.l1, self.l2, self.l3, self.l4, self.l5]
            self.lineSet2 = [self.l6, self.l7, self.l8, self.l9]
            self.lineSet3 = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8, self.l9]

    def test_ExtremePoints_1(self):
          test = LineArrangement(self.lineSet1)
          self.assertEqual(test.extremePoints(), (Fraction(5, 9), 13, 125, Fraction(-13, 3)))

    def test_ExtremePoints_2(self):
        test = LineArrangement(self.lineSet2)
        self.assertEqual(test.extremePoints(), (Fraction(5, 3), Fraction(24, 1), Fraction(16, 1), Fraction(10, 9)))

    def test_ExtremePoints_3(self):
        test = LineArrangement(self.lineSet3)
        self.assertEqual(test.extremePoints(), (0, 24, 125, -17))

    def test_boundingBox_1(self):
         result = self.boundingBoxSetUp(Fraction(5, 9), 13, 125, Fraction(-13, 3))
         self.assertEqual(None, result, result)

    def test_boundingBox_2(self):
         result = self.boundingBoxSetUp(Fraction(5, 3), Fraction(24, 1), Fraction(16, 1), Fraction(10, 9))
         self.assertEqual(None, result, result)

    def test_boundingBox_3(self):
         result = self.boundingBoxSetUp(0, 24, 125, -17)
         self.assertEqual(None, result, result)

    def test_edgeInt_1(self):
         LA = LineArrangement(None)
         edge = HalfEdge(Vertex((Fraction(-1, 3), 0), None), Vertex((3, 10), None), None, None, None, None)
         edgeLineInt = [None, (Fraction(6, 7), Fraction(25, 7)), (Fraction(36, 13), Fraction(121, 13)), (Fraction(4, 3), 5), None, None, (Fraction(6, 5), Fraction(23, 5)), None, None]
         for i, line in enumerate(self.lineSet3):
              self.assertEqual(edgeLineInt[i], LA.lineEdgeInt(line, edge), f"Error: line edge intercept, line #{i+1}. \nExpected: {edgeLineInt[i]}, but got: {LA.lineEdgeInt(line, edge)}")

    def test_leftMostEdge_1(self):
         LA = LineArrangement(self.lineSet2)
         LA.boundingBox(Fraction(5,3), 24, 16, Fraction(10,9))
         leftTop = (Fraction(5, 3), 16)
         rightTop = (24, 16)
         leftBottom = (Fraction(5, 3), Fraction(10, 9))
         rightBottom = (24, Fraction(10, 9))
         expected_origin = [leftBottom, leftBottom, leftBottom, leftBottom, rightBottom]
         expected_dest = [leftTop, leftTop, leftTop, leftTop, leftBottom]
         for i, line in enumerate(self.lineSet1):
              result = LA.leftMostedge(line)
              result_origin = result.origin().coord()
              result_dest = result.dest().coord()
              self.assertEqual((result_origin, result_dest), (expected_origin[i], expected_dest[i]), f"Error in leftmost edge with line {i+1}. Expected: {expected_origin[i]}->{expected_dest[i]}.Result: {result_origin}->{result_dest}")


    def test_addLine__perimeter_1(self):
        line = Line((0, 1), (4, 9))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(0, 10), (Fraction(9, 2), 10), (10, 10), (10, 0), (0, 0), (0, 1)]
        result_vertices = self.perimeterTraversal(LA, (0, 10))
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine_perimeter_2(self):
        line = Line((3, 0), (0, 12))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(0, 10), (Fraction(1, 2), 10), (10, 10), (10, 0), (3, 0),(0, 0)]
        result_vertices = self.perimeterTraversal(LA, (0, 10))
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine_perimeter_3(self):
        line = Line((16, 0), (0, 8))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(0, 10), (10, 10), (10, 3), (10, 0), (0, 0), (0, 8)]
        result_vertices = self.perimeterTraversal(LA, (0, 10))
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine_perimeter_4(self):
        l1 = Line((0, 1), (4, 9))
        l2 = Line((3, 0), (0, 12))
        LA = LineArrangement([l1, l2])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(l1)
        LA.addLine(l2)
        expected_vertices = [(0, 10), (Fraction(1, 2), 10), (Fraction(9, 2), 10), (10, 10), (10, 0), (3, 0), (0, 0), (0, 1)]
        result_vertices = self.perimeterTraversal(LA, (0, 10))
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine_perimeter_5(self):
        l1 = Line((0, 1), (1, 3))
        l2 = Line((2, 10), (2, 100))
        l3 = Line((0, 5), (10, 5))
        l4 = Line((0, -3), (1, 1))
        LA = LineArrangement([l1, l2, l3, l4])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(l1)
        LA.addLine(l2)
        LA.addLine(l3)
        LA.addLine(l4)
        expected_vertices = [(0, 10), (2, 10), (Fraction(13, 4), 10), (Fraction(9, 2), 10), (10, 10), (10, 5), (10, 0), (2, 0), (Fraction(3, 4), 0), (0,0), (0, 1), (0, 5)]
        result_vertices = self.perimeterTraversal(LA, (0, 10))
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine__line_intersections_1(self):
        line = Line((0, 1), (4, 9))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(0, 1), (Fraction(9, 2), 10)]
        result_vertices = self.lineTraversal(LA, line)
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine__line_intersections_2(self):
        line = Line((0, 12), (3, 0))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(Fraction(1, 2), 10), (3, 0)]
        result_vertices = self.lineTraversal(LA, line)
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine__line_intersections_3(self):
        line = Line((0, 0), (2, 10))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(0, 0), (2, 10)]
        result_vertices = self.lineTraversal(LA, line)
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine__line_intersections_4(self):
        l1 = Line((0, 1), (4, 9))
        l2 = Line((0, 12), (3, 0))
        LA = LineArrangement([l1, l2])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(l1)
        LA.addLine(l2)
        # print(self.perimeterTraversal(LA, (0, 10)))
        expected_vertices = [(Fraction(1, 2), 10), (Fraction(11, 6), Fraction(14, 3)), (3, 0)]
        result_vertices = self.lineTraversal(LA, l2)
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")

    def test_addLine__line_intersections_5(self):
        l1 = Line((0, 1), (4, 9))
        l2 = Line((0, 12), (3, 0))
        l3 = Line((0, 0), (1, 5))
        LA = LineArrangement([l1, l2, l3])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(l1)
        LA.addLine(l2)
        LA.addLine(l3)
        # print(self.perimeterTraversal(LA, (0, 10)))
        expected_vertices = [(0, 0), (Fraction(1, 3), Fraction(5, 3)), (Fraction(4, 3), Fraction(20, 3)), (2, 10)]
        result_vertices = self.lineTraversal(LA, l3)
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")


    def test_addLine_interiorFaces_1(self):
        line = Line((0, 1), (4, 9))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        leftFaceVertices = [(0, 1), (0, 0), (10, 0), (10, 10), (Fraction(9, 2), 10)]

        leftEdge = LA.leftMostedge(line).twin()

        leftResultVertices = self.faceTraversal(LA, leftEdge)


        for i, leftCoord in enumerate(leftFaceVertices):
            self.assertEqual(leftCoord, leftResultVertices[i], f"Error in left face: expected: {leftFaceVertices}. But result: {leftResultVertices}")


    def test_addLine_interiorFaces_2(self):
        line = Line((0, 1), (4, 9))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        rightFaceVertices = [(0, 10), (0, 1), (Fraction(9, 2), 10)]
        rightEdge = LA.leftMostedge(line).next().twin()
        rightResultVertices = self.faceTraversal(LA, rightEdge)

        for i, rightCoord in enumerate(rightFaceVertices):
            self.assertEqual(rightCoord, rightResultVertices[i], f"Error in right face: expected: {rightFaceVertices}. But result: {rightResultVertices}")


    def test_addLine_interiorFaces_3(self):
        l1 = Line((0, 1), (1, 3))
        l2 = Line((2, 10), (2, 100))
        l3 = Line((0, 5), (10, 5))
        l4 = Line((0, -3), (1, 1))
        LA = LineArrangement([l1, l2, l3, l4])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(l1)
        LA.addLine(l2)
        LA.addLine(l3)
        LA.addLine(l4)
        leftEdge = LA.leftMostedge(l4).twin()
        leftFaceVertices = [(Fraction(3, 4), 0), (2, 0), (2, 5)]
        leftResultVertices = self.faceTraversal(LA, leftEdge)
        for i, leftCoord in enumerate(leftFaceVertices):
            self.assertEqual(leftCoord, leftResultVertices[i], f"Error in left face: expected: {leftFaceVertices}. But result: {leftResultVertices}")

    def test_maxDegree(self):
        l1 = Line((0, 0), (2, 2))
        l2 = Line((0, -8), (2, 2))
        l3 = Line ((0, 22), (2, 2))
        l4 = Line((0, 2), (2, 2))
        l5 = Line((0,0), (6, 1))
        l6 = Line((0, 20), (1, 13))


        LA = LineArrangement([l1, l2, l3, l4, l5, l6])
        print(LA.extremePoints())
        LA.constructArrangement()
        expected = 4
        result = LA.maxIntersection()
        self.assertEqual(expected, result, f"Error: expected max intersection={expected} but result={result}")

    def perimeterTraversal(self, LA: LineArrangement, start: tuple):
        """Output a list of visited coordinates on the outside face."""
        edge = LA.outsideEdge
        # print("\nOutside edge:", edge.toString())
        while (edge.origin().coord() != start):
            edge = edge.next()

        # print(edge.toString())
        edgeList = [edge.origin().coord()]
        edge = edge.next()
        while edge.origin().coord() != edgeList[0]:
            edgeList.append(edge.origin().coord())
            edge = edge.next()
            # print(f"edge: {edge.toSring()}, {edge}. \nNext edge: {edge.next().toSring()}, {edge.next()}")
        return edgeList


    def faceTraversal(self, LA: LineArrangement, edge: HalfEdge):
        """traverse the vertices of a face"""
        vertexList = [edge.origin().coord()]
        edge = edge.next()
        count = 0
        while edge.origin().coord() != vertexList[0]:
            vertexList.append(edge.origin().coord())
            edge = edge.next()
            count +=1

        return vertexList


    def lineTraversal(self, LA: LineArrangement, line: Line) -> list[tuple]:
        """Output a list of vertices on the given line in the line arrangement"""
        edge = LA.leftMostedge(line).twin()  # twin so we get interior egde
        vertexList = [edge.origin().coord()]
        # while edge is on a bounded face:
        while edge.boundedFace():
            # find next edge with an intersection with line
            # print(f"\nedge: {edge.toString()}\nnextEdge: {edge.next().toString()}")
            edge = edge.next()
            intersection = LA.lineEdgeInt(line, edge)
            while intersection is None:
                # print(f"\nedge: {edge.toString()}\nnextEdge: {edge.next().toString()}")
                edge = edge.next()
                intersection = LA.lineEdgeInt(line, edge)

            if intersection != vertexList[-1]:
                vertexList.append(intersection)

            edge = edge.twin()
            # print(edge.toSring())
            # print(edge.incFace().outComp())

        return vertexList


    def boundingBoxSetUp(self, left, right, top, bottom):
        test = LineArrangement(None)
        test.boundingBox(left, right, top, bottom)
        corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
        edge = test.outsideEdge

        # check if edge is initialized properly
        if edge.origin().coord() != (left, top) or edge.dest().coord() != (right, top):
            return f"Error: outside edge not initialized properly. \nResult origin: {edge.origin().coord()}: Expected origin: {(left, top)}\nResult dest: {edge.dest().coord()}: Expected dest: {(right, top)}"


        # traverse clockwise around the outside ():
        for i in range(5):
            index = i%4
            if edge.origin().coord() != corners[index]:
                return f"Error, outside edges: expected origin: {corners[index]} but was {edge.origin().coord()}"

            edge = edge.next()

        # traverse the interior of the box counter-clockwise
        edge = edge.twin().next().next() # want first edge to ahve origin (left, top)
        for i in range(4, -1, -1):
            index = i%4

            if edge.origin().coord() != corners[index]:
                return f"Error, inside edges: expected origin: {corners[index]} but was {edge.origin().coord()}"

            edge = edge.next()

        return None
