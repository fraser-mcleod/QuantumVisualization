import LineArrangement as LA
from fractions import Fraction


def main():
    # create line set
    l1 = LA.Line((0, -4), (4, 0))   # y = x - 4
    l2 = LA.Line((0, 6), (3, 0))    # y = -2x + 6
    l3 = LA.Line((0, 0), (4, 1))    # y = x/4
    l4 = LA.Line((0, 14), (7, 0))   # y = -2x + 14
    l5 = LA.Line((0, 5), (8, 4))    # y = -x/8 + 5
    l6 = LA.Line((0, 2), (6, 2))    # y = 2
    lineSet = [l1, l2, l3, l4, l5, l6]
    # construct line arrangement
    lineArrangement = LA.LineArrangement(lineSet)
    extremePoints = lineArrangement.extremePoints()
    lineArrangement.constructArrangement()
    maxVertexCoord = lineArrangement.maxIntersectionVertex().coord()
    maxIntersection = lineArrangement.maxIntersection()
    # print results
    print("---Creating Line Arrangement with lines:---")
    for line in lineSet:
        print(line.toString())
    print(f"The bounding box has sides: left={extremePoints[0]}, right={extremePoints[1]}, top={extremePoints[2]}, bottom={extremePoints[3]}")
    print(f"The maximum line intersection is: {maxIntersection} at the point: {maxVertexCoord}")

if __name__ == "__main__":
    main()