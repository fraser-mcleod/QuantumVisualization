import unittest

from src.QLines import *

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
         rightBottom = (Fraction(24, Fraction(10, 9)))
         expected_origin = [leftBottom, leftBottom, leftBottom, leftBottom, leftTop]
         expected_dest = [leftTop, leftTop, leftTop, leftTop, rightTop]
         for i, line in enumerate(self.lineSet1):
              result = LA.leftMostedge(line)
              result_origin = result.origin().coord()
              result_dest = result.dest().coord()
              self.assertEqual((result_origin, result_dest), (expected_origin[i], expected_dest[i]), f"Error in leftmost edge with line {i+1}. \nExpected: {expected_origin[i]}->{expected_dest[i]}.\nResult: {result_origin}->{result_dest}")


    def test_line_arrangement_1(self):
        line = Line((0, 1), (4, 9))
        LA = LineArrangement([line])
        LA.boundingBox(0, 10, 10, 0)
        LA.addLine(line)
        expected_vertices = [(0, 10), (Fraction(9, 2), 10), (10, 10), (10, 0), (0, 0), (0, 1)]
        result_vertices = self.perimeterTraversal(LA, (0, 10))
        for i, expected in enumerate(expected_vertices):
             self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")


    def perimeterTraversal(self, LA: LineArrangement, start: tuple):
        """Output a list of visited coordinates on the outside face."""
        edge = LA.outsideEdge
        while (edge.origin().coord() != start):
            edge = edge.next()


        edgeList = [edge.origin().coord()]
        edge = edge.next()
        while edge.origin().coord() != edgeList[0]:
            edgeList.append(edge.origin().coord())
            edge = edge.next()
            # print(f"edge: {edge.toSring()}, {edge}. \nNext edge: {edge.next().toSring()}, {edge.next()}")
        return edgeList


    def lineTraversal(self, LA: LineArrangement, line: Line):
         """Output a list of vertices on the given line in the line arrangement"""
         edge = LA.leftMostedge(line).twin()  # twin so we get interior egde
         edgeList = [edge.origin().coord()]






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
