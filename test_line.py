import unittest

from src.QLines import *


class TestLine(unittest.TestCase):
    def setUp(self):
        self.l1 = Line((0, 0), (1, 1))
        self.l2 = Line((0, -5), (1, 5))
        self.l3 = Line((Fraction(39, 4), 0), (0, 13))
        self.l4 = Line((10, 5), (20, 5))
        self.l5 = Line((13, 0), (13, 100))
        self.lines = [self.l1, self.l2, self.l3, self.l4, self.l5]

        self.slopes = [1, 10, Fraction(-4, 3), 0, None]
        self.yInt = [0, -5, 13, 5, None]
        self.xInt = [0, Fraction(1, 2), Fraction(13*3, 4), None, 13]
        self.isHorizontal = [False, False, False, True, False]
        self.isVertical = [False, False, False, False, True]

        self.l1Intersections = (None, (Fraction(5, 9), Fraction(5, 9)), (Fraction(39, 7), Fraction(39, 7)), (5, 5), (13, 13))
        self.l2Intersections = ((Fraction(5, 9), Fraction(5, 9)), None, (Fraction(27, 17), Fraction(185, 17)), (1, 5), (13, 125))

    def test_slope(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.slopes[i], line.slope(), f"Error: slope wrong for line {i+1}")

    def test_yInt(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.yInt[i], line.yInt(), f"Error: yInt wrong for line {i+1}")

    def test_xInt(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.xInt[i], line.xInt(), f"Error: xInt wrong for line {i+1}")

    def test_isHorizontal(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.isHorizontal[i], line.isHorizontal(), f"Error: isHorizontal wrong for line {i+1}")

    def test_isVertical(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.isVertical[i], line.isVertical(), f"Error: isVertical wrong for line {i+1}")

    def test_l1_intersection(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.l1.intercept(line), self.l1Intersections[i], f"Error: l1, l{i+1} intersection is wrong")

    def test_l2_intersection(self):
        for i, line in enumerate(self.lines):
            self.assertEqual(self.l2.intercept(line), self.l2Intersections[i], f"Error: l2, l{i+1} intersection is wrong")