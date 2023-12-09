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
          self.assertEquals(test.extremePoints(), (Fraction(5/9), 13, 13, Fraction(-13, 3)))