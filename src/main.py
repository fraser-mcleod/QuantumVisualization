import QLines

from time import sleep
from fractions import Fraction

def test_ExtremePoints(lines: list[QLines.Line], expected: tuple):
    """A test a single instance of computing extreme points. No output implies success."""
    test = QLines.LineArrangement(lines)
    result = test.extremePoints()
    if result != expected:
        print("Error in extreme points! Expected: ", expected, "but got: ", result)

def test_boundingBox(left, right, top, bottom):
    """Test a single case of forming a bounding box. No output imples success."""
    test = QLines.LineArrangement(None)
    test.boundingBox(left, right, top, bottom)
    corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
    unboundedFace = test.faceRecord[0]
    # if face is unbounded
    if unboundedFace.outComp is None:
        boundedFace = test.faceRecord[1]
    else:
        unboundedFace = test.faceRecord[1]
        boundedFace = test.faceRecord[0]

    # test bounded face by traversing its edges
    # edge = boundedFace.outComp()
    edge = test.outsideEdge
    cur_coord = edge.origin().coord()
    # find cur_coord in corners
    start = 0
    for i, coord in enumerate(corners):
        if cur_coord == coord:
            start = i
            break
    # make sure the traversak is correct
    for j in range(5):
        index = (start-j)%4  # subtract j as we want to go counter clockwise
        if cur_coord != corners[index]:
            print("Error in bounded face!")
            exit()
        edge = edge.next()
        cur_coord = edge.origin().coord()

    # test unbounded face by traversing its edges
    edge = edge.twin()  # we know there should only be two faces
    cur_coord = edge.origin().coord()
    # find cur_coord in corners
    start = 0
    for i, coord in enumerate(corners):
        if cur_coord == coord:
            start = i
            break
    # make sure the traversak is correct
    for j in range(5):
        index = (start+j)%4  # add j to move clockwise
        if cur_coord != corners[index]:
            print("Error in unbounded face!")
            exit()
        edge = edge.next()
        cur_coord = edge.origin().coord()








def main():
    # print(None)
    # # test_boundingBox(10, 40, 30, 0)
    # # test_boundingBox(-100, 40.5, 36, -0.1)
    # l1 = QLines.Line((1, 0), (10, 15))
    # l2 = QLines.Line((6, 7), (8, 8))
    # l3 = QLines.Line((14, 0), (11, 6))
    # l4 = QLines.Line((6, 4), (0, 0))
    # lines = [l1, l2, l3, l4]
    # expected = (Fraction(5, 3), Fraction(24, 1), Fraction(16, 1), Fraction(10, 9))
    # test_ExtremePoints(lines, expected)

    # LA = QLines.LineArrangement(lines)
    # corners = LA.extremePoints()
    # LA.boundingBox(corners[0], corners[1], corners[2], corners[3])
    # LA.lineArrangement()
    l1 = QLines.Line((0, 1), (4, 9))
    l2 = QLines.Line((3, 0), (0, 12))
    LA = QLines.LineArrangement([l1, l2])
    LA.boundingBox(0, 10, 10, 0)
    LA.addLine(l1)
    LA.addLine(l2)
    expected_vertices = [(0, 10), (Fraction(1, 2), 10), (Fraction(9, 2), 10), (10, 10), (10, 0), (3, 0), (0, 0), (0, 1)]
    # result_vertices = self.perimeterTraversal(LA, (0, 10))
    # for i, expected in enumerate(expected_vertices):
    #         self.assertEqual(expected, result_vertices[i], f"Error in line arrangement, index {i}.\nExpected: {expected_vertices}\nResult: {result_vertices}")


if __name__ == "__main__":
    main()