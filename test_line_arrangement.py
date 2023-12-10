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
